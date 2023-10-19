from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# Register your models here.
from .models import User, Category, Listing, Bid, Comment, Watchlist


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'category')


class ListingAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'creator', 'category', 'active', 'sold', 'price', 'winner')
    list_filter = ('active', 'sold', 'category')
    search_fields = ('title', 'description')


class BidAdmin(admin.ModelAdmin):
    list_display = ('id', 'listing', 'bidder', 'price')
    list_filter = ('listing', 'bidder')


class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'listing', 'timestamp')
    list_filter = ('user', 'listing', 'timestamp')
    search_fields = ('comment',)
    ordering = ('-timestamp',)  # Note the '-' prefix which means descending order


class WatchlistAdmin(admin.ModelAdmin):
    filter_horizontal = ('listings',)
    list_display = ('id', 'user')
    list_filter = ('user',)


admin.site.register(User, UserAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Listing, ListingAdmin)
admin.site.register(Bid, BidAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Watchlist, WatchlistAdmin)
