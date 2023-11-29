from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    # Direct method to count number of followers
    def count_followers(self):
        return Follow.objects.filter(user=self).count()

    def count_following(self):
        return Follow.objects.filter(follower=self).count()

    pass


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name="liked_posts", blank=True)

    # Direct method to count the number of likes on the post
    def count_likes(self):
        return self.likes.count()

    # Meta class to order posts in reverse chronological order
    class Meta:
        ordering = ['-timestamp']


class Follow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followers")
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following")
