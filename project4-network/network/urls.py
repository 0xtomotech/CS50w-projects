
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("user/<str:user_name>", views.user_view, name="user_page"),
    path("toggle_follow/<str:user_name>", views.toggle_follow, name="toggle_follow"),
    path("following", views.following_view, name="following"),
    path("post/<int:post_id>/edit", views.post_edit, name="post_edit"),
    path("post/<int:post_id>/like", views.toggle_like, name="toggle_like"),
]
