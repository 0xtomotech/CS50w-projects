from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("createlisting/", views.createlisting, name="createlisting"),
    path("listing/<str:listing_id>", views.listing, name="listing"),
    path("listing/<int:listing_id>/bid", views.bid_on_listing, name="listing_bid"),
    path("toggle_watchlist/<str:listing_id>/", views.toggle_watchlist, name='toggle_watchlist'),
    path("close_auction/<int:listing_id>/", views.close_auction, name='close_auction'),
    # IMPORTANT NOTICE LAST MINUTE watchlist implementation is NOT secure, as the below implementation via user_id
    # can mean that any logged in person can get anyone's watchlist, as there is currently no server side validation.
    # BETTER IMPLEMENTATION: wonauctions
    path("watchlist/<int:user_id>/", views.watchlist, name="watchlist"),
    path("category/", views.category, name='category'),
    path("wonauctions/", views.won_auctions, name="won_auctions")
]
