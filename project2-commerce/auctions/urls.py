from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register")
]

# TODO: create create listing page
# TODO: create individual listing page
# TODO: create watchlist page for logged in users
# TODO: create categories page for logged in users

