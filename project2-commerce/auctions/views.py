from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import User, Listing, Category, Bid, Watchlist, Comment
from .forms import CreateListingForm, BidForm, CommentForm, CategoryFilterForm


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
                image_url = 'https://t3.ftcdn.net/jpg/02/48/42/64/360_F_248426448_NVKLywWqArG2ADUxDq6QprtIzsF82dMF.jpg'
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
    comment_form = CommentForm()
    comments = Comment.objects.filter(listing=listing).order_by('-timestamp')
    bids = Bid.objects.filter(listing=listing).order_by('-price')

    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = Comment(
                user=request.user,
                listing=listing,
                comment=comment_form.cleaned_data['content']
            )
            comment.save()
            return redirect('listing', listing_id)


    else:
        # Get method
        return render(request, "auctions/listing.html", {
            "listing": listing,
            "is_owner": is_owner,
            "bid_form": bid_form,
            "bids": bids,
            "comment_form": comment_form,
            "comments": comments
        })



@login_required
def bid_on_listing(request, listing_id):
    listing = Listing.objects.get(id=listing_id)
    bids = Bid.objects.filter(listing=listing).order_by('-price')
    comment_form = CommentForm()
    comments = Comment.objects.filter(listing=listing).order_by('-timestamp')
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
                    "bids": bids,
                    "comment_form": comment_form,
                    "comments": comments
                })
            else:
                # render listing page with error message displayed in listing html
                return render(request, "auctions/listing.html", {
                    "listing": listing,
                    "is_owner": (listing.creator == request.user),
                    "bid_form": form,
                    "message": "Your bid should be higher than the current price!",
                    "bids": bids,
                    "comment_form": comment_form,
                    "comments": comments
                })
        else:
            return render(request, "auctions/listing.html", {
                "listing": listing,
                "is_owner": (listing.creator == request.user),
                "bid_form": form,
                "message": "Invalid form input. Please try again.",
                "bids": bids,
                "comment_form": comment_form,
                "comments": comments
            })
    # Handle GET requests
    return redirect('listing', listing_id=listing_id)


@login_required
def toggle_watchlist(request, listing_id):
    user = request.user
    if not user.is_authenticated:
        # If the user is not authenticated, redirect them to login
        return redirect("login")
    listing = Listing.objects.get(pk=listing_id)
    # Check if the user already has a Watchlist instance
    watchlist, created = Watchlist.objects.get_or_create(user=user)
    # If the listing is already in the user's watchlist, remove it
    if listing in watchlist.listings.all():
        watchlist.listings.remove(listing)
    # Otherwise, add it
    else:
        watchlist.listings.add(listing)

    return redirect('listing', listing_id=listing_id)


@login_required
def watchlist(request, user_id):
    user = User.objects.get(id=user_id)
    watchlist, created = Watchlist.objects.get_or_create(user=user)
    return render(request, "auctions/watchlist.html", {
        "listings": watchlist.listings.all()
    })



@login_required()
def won_auctions(request):
    user = request.user
    won_listings = Listing.objects.filter(winner=user)
    return render(request, "auctions/wonauctions.html", {
        "listings": won_listings
    })

def category(request):
    form = CategoryFilterForm(request.GET or None)
    listings = Listing.objects.all()
    # or None part is a fallback. If request.GET is empty, then None will be used as the value
    if form.is_valid():
        category = form.cleaned_data['category']
        if category:
            listings = Listing.objects.filter(category=category)


    return render(request, "auctions/category.html", {
        "form": form,
        "listings": listings
    })


@login_required()
def close_auction(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    # Ensure that the user trying to close the auction is the creator of the listing
    if request.user == listing.creator and listing.active:
        highest_bid = Bid.objects.filter(listing=listing).order_by('-price').first()
        if highest_bid:
            listing.winner = highest_bid.bidder
            listing.sold = True
            listing.active = False
            listing.save()

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
