from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.models import User
from  inquiry.models import Inquiry

# Create your views here.

# register view


def register(request):
    if request.method == 'POST':
        # get form values
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        # check if passwords match
        if password == password2:
            # check username
            if User.objects.filter(username=username).exists():
                messages.error(request, 'username alraedy exist')
                return redirect('register')
            else:
                # check email
                if User.objects.filter(email=email).exists():
                    messages.error(request, 'that email is being used')
                    return redirect('register')
                else:
                    user = User.objects.create_user(
                        username=username, password=password, email=email, first_name=first_name, last_name=last_name)
                    user.save()
                    messages.success(
                        request, 'Registration succesfull and can login')
                    return redirect('login')
        else:
            messages.error(request, 'passwords do not match')
            return redirect('register')
    else:
        return render(request, 'accounts/register.html')


# login view
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            messages.success(request, 'login succesful')
            return redirect('dashboard')
        else:
            messages.error(request, 'invalid credentials')
            return redirect('login')
    else:
        return render(request, 'accounts/login.html')


def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        messages.success(request, 'logout succesfull')
    return redirect('index')


def dashboard(request):
    #get the inquiries from the database and filter by the current logged in user
    user_inquiry = Inquiry.objects.order_by('-contact_date').filter(user_id=request.user.id)
    context={
        'user_inquiry':user_inquiry
    }
    return render(request, 'accounts/dashboard.html',context)
