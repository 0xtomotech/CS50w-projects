from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Email


# Register your models here.
class EmailAdmin(admin.ModelAdmin):
    list_display = ('user', 'sender', 'subject', 'timestamp', 'read', 'archived')


admin.site.register(User, UserAdmin)
admin.site.register(Email, EmailAdmin)
