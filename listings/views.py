from django.shortcuts import render, get_object_or_404
from . models import Listing
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from listings.choices import bedroom_choices, price_choices, state_choices
# Create your views here.


def index(request):
    listings = Listing.objects.all().order_by(
        '-list_date').filter(is_published=True)
    paginator = Paginator(listings, 3)
    page = request.GET.get('page')
    paged_listings = paginator.get_page(page)
    context = {'listings': paged_listings}
    return render(request, 'listings/listings.html', context)


def listing(request, listing_id):
    listing = get_object_or_404(Listing, id=listing_id)
    context = {'listing': listing}
    return render(request, 'listings/listing.html', context)


def search(request):
    listings = Listing.objects.order_by('-list_date')


# keywords search
    if 'keywords' in request.GET:
        keywords = request.GET['keywords']
        if keywords:
            # match keyword request with description field in database
            listings = listings.filter(description__icontains=keywords)

# bedrooms search
# lte means less than or equal to
    if 'bedrooms' in request.GET:
        bedrooms = request.GET['bedrooms']
        if bedrooms:
            # match bedroom request with bedroom field in database
            listings = listings.filter(bedrooms__lte=bedrooms)


# state search
    if 'state' in request.GET:
        state = request.GET['state']
        if state:
            # match state request with state field in database
            listings = listings.filter(state__iexact=state)


# price search
    if 'price' in request.GET:
        price = int(request.GET['price'])
        if price:
            # match price request with price field in database
            listings = listings.filter(price__lte=price)


# city search
    if 'city' in request.GET:
        city = request.GET['city']
        if city:
            # match city request with city field in database
            listings = listings.filter(city__iexact=city)
    context = {
        'bedroom_choices': bedroom_choices,
        'state_choices': state_choices,
        'price_choices': price_choices,
        'listings': listings,
        'values': request.GET
    }
    return render(request, 'listings/search.html', context)
