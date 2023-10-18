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
    path("watchlist/<int:user_id>/", views.watchlist, name="watchlist"),
    path("category/", views.category, name='category')
]

# TODO: create watchlist page for logged in users
# TODO: create categories page for logged in users

