from django.shortcuts import render, redirect
from . models import Inquiry
from django.contrib import messages
from django.core.mail import send_mail

# Create your views here.


def inquiry(request):
    if request.method == 'POST':
        listing_id = request.POST['listing_id']
        listing = request.POST['listing']
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        message = request.POST['message']
        user_id = request.POST['user_id']
        realtor_email = request.POST['realtor_email']

        # check if user has made an inquiry already
        if request.user.is_authenticated:
            user_id = request.user.id
            has_contacted = Inquiry.objects.all().filter(
                listing_id=listing_id, user_id=user_id)
            if has_contacted:
                messages.error(
                    request, 'you have alraedy made an inquiry for this listing')
                return redirect('/listings/' + listing_id)

        contact = Inquiry(listing=listing, listing_id=listing_id,
                          name=name, email=email, phone=phone, message=message, user_id=user_id)
        contact.save()
        #send mail
        send_mail(
            'property listing inquiry',
            'there has been an inquiry for ' + listing + '. sign into the admin panel for more info',
            'princewillowoh18@gmail.com',
            [realtor_email],
            fail_silently = false
        )
        messages.success(
            request, 'your request has been submitted, a realtor will get back to you soon')

    return redirect('/listings/' + listing_id)
