from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseAdmin
from .models import User, Post, Follow


#
class UserAdmin(BaseAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'count_followers', 'count_following')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    readonly_fields = ('date_joined', 'last_login')


#


admin.site.register(User, UserAdmin)


class PostAdmin(admin.ModelAdmin):
    list_display = ('user', 'timestamp', 'content', 'count_likes')
    list_filter = ('timestamp', 'user')
    search_fields = ('content', 'user__username')


admin.site.register(Post, PostAdmin)


class FollowAdmin(admin.ModelAdmin):
    list_display = ('user', 'follower')
    list_filter = ('user', 'follower')
    search_fields = ('user__username', 'follower__username')


admin.site.register(Follow, FollowAdmin)
