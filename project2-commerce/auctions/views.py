from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import User, Listing, Category, Bid
from .forms import CreateListingForm, BidForm

# TODO: listing should also render watched by section

#TODO: default index route to render all active auction listings
def index(request):

    return render(request, "auctions/index.html", {
        "listings": Listing.objects.filter(sold=False)
    })

@login_required
def createlisting(request):
    if request.method == "POST":
        form = CreateListingForm(request.POST)
        if form.is_valid():
            # Check if a new category is provided or an existing one is selected
            category_selected = form.cleaned_data['categories']
            new_category = form.cleaned_data['new_category']
            if not category_selected and new_category:
                # Create the new category and assign it
                category_obj, _ = Category.objects.get_or_create(category=new_category)
            elif category_selected:
                category_obj = category_selected
            else:
                # This means neither a new category was provided nor an existing one selected
                # For now, I'll just redirect to the same page.
                return redirect('createlisting')

            # Check if image_url is provided by user, if not assign a placeholder
            image_url = form.cleaned_data['image_url']
            if not image_url:
                image_url = 'placeholderimageurl.jpg'
            # Create a new listing
            listing = Listing(
                creator=request.user,
                title=form.cleaned_data['title'],
                description=form.cleaned_data['description'],
                price=form.cleaned_data['bid'],
                image_url=image_url,
                category=category_obj
            )
            listing.save()

            return redirect('index')
    # Get Request, load page and form
    else:
        form = CreateListingForm()

    return render(request, "auctions/createlisting.html", {
            'listing_form': form
        })


def listing(request, listing_id):
    listing = Listing.objects.get(id=listing_id)
    user = request.user
    is_owner = True if listing.creator == user else False
    bid_form = BidForm()
    bids = Bid.objects.filter(listing=listing).order_by('-price')

    return render(request, "auctions/listing.html", {
        "listing": listing,
        "is_owner": is_owner,
        "bid_form": bid_form,
        "bids": bids
    })



def bid_on_listing(request, listing_id):
    listing = Listing.objects.get(id=listing_id)
    bids = Bid.objects.filter(listing=listing).order_by('-price')
    if request.method == "POST":
        form = BidForm(request.POST)
        if form.is_valid():
            bid_amount = form.cleaned_data['bid_amount']

            # Check if bid meets requirements
            if listing.price < bid_amount:
                # Accept bid
                listing.price = bid_amount # update listing price
                listing.save()
                Bid.objects.create(listing=listing, bidder=request.user, price=bid_amount)
                return render(request, "auctions/listing.html", {
                    "listing": listing,
                    "is_owner": (listing.creator == request.user),
                    "bid_form": form,
                    "message": "Bid sucessfully placed!",
                    "bids": bids
                })
            else:
                # render listing page with error message displayed in listing html
                return render(request, "auctions/listing.html", {
                    "listing": listing,
                    "is_owner": (listing.creator == request.user),
                    "bid_form": form,
                    "message": "Your bid should be higher than the current price!",
                    "bids": bids
                })
        else:
            return render(request, "auctions/listing.html", {
                "listing": listing,
                "is_owner": (listing.creator == request.user),
                "bid_form": form,
                "message": "Invalid form input. Please try again.",
                "bids": bids
            })
    # Handle GET requests
    return redirect('listing', listing_id=listing_id)


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
