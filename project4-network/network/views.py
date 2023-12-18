import json

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator

from .models import User, Post, Follow


def index(request):
    post_list = Post.objects.all()
    paginator = Paginator(post_list, 10)

    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    return render(request, "network/index.html", {
        "page_obj": page_obj
    })


def following_view(request):
    current_user = request.user
    # fetch users that current user is following
    users_on_feed = User.objects.filter(followers__follower=current_user)
    # fetch posts from these users
    post_list = Post.objects.filter(user__in=users_on_feed).order_by('-timestamp')
    paginator = Paginator(post_list, 10)

    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    return render(request, "network/following.html", {
        "page_obj": page_obj
    })


def user_view(request, user_name):
    user_profile = User.objects.get(username=user_name)
    posts = Post.objects.filter(user=user_profile).order_by('-timestamp')
    current_user = request.user

    # Check if current user follows the profile
    is_following = False
    if current_user.is_authenticated and Follow.objects.filter(user=user_profile, follower=current_user).exists():
        is_following = True

    context = {
        'user_profile': user_profile,
        'posts': posts,
        'is_following': is_following,
        'followers_count': user_profile.count_followers(),
        'following_count': user_profile.count_following()
    }

    return render(request, "network/user.html", context)


@login_required
def new_post(request):
    if request.method == "POST":
        data = json.loads(request.body)
        content = data.get('content')

        if content:
            Post.objects.create(user=request.user, content=content)
            return JsonResponse({"message": "Post created successfully."}, status=201)
        else:
            return JsonResponse({"error": "Content cannot be empty!"}, status=400)
    return JsonResponse({"error": "POST request required."}, status=400)


@login_required
def toggle_follow(request, user_name):
    if request.method == "POST":
        current_user = request.user
        try:
            user_to_follow = User.objects.get(username=user_name)
        except User.DoesNotExist:
            return HttpResponseRedirect(reverse('index'))

        # Check if current user already follows the account
        existing_follow = Follow.objects.filter(user=user_to_follow, follower=current_user).first()
        if existing_follow:
            # Unfollow user
            existing_follow.delete()
        else:
            # Follow user
            Follow(user=user_to_follow, follower=current_user).save()

    return HttpResponseRedirect(reverse('user_page', args=[user_name]))


@login_required
def toggle_like(request, post_id):
    if request.method == "POST":
        try:
            post = Post.objects.get(id=post_id)
            if request.user in post.likes.all():
                post.likes.remove(request.user)
                liked = False
            else:
                post.likes.add(request.user)
                liked = True
            return JsonResponse({
                "liked": liked,
                "likes_count": post.likes.count()
            }, status=200)
        except Post.DoesNotExist:
            return JsonResponse({"error": "Post not found."}, status=404)
    return JsonResponse({"error": "POST request required."}, status=400)


@login_required
def post_edit(request, post_id):
    if request.method == "POST":
        try:
            post = Post.objects.get(id=post_id, user=request.user)  # Ensuring only the author can edit the post
            data = json.loads(request.body)  # Load data from json
            content = data.get('content')
            if content:
                post.content = content
                post.save()
                return JsonResponse({"message": "Post updated successfully."}, status=200)
            else:
                return JsonResponse({"error": "Content cannot be empty!"}, status=400)
        except Post.DoesNotExist:
            return JsonResponse({"error": "Post not found..."}, status=404)
    else:
        return JsonResponse({"error": "POST request required!"}, status=400)


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
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


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
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
