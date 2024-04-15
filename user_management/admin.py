
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    # model = CustomUser
    # list_display = ['username', 'email', 'created_at', 'updated_at']
    # search_fields = ['username', 'email']
    # readonly_fields = ['created_at', 'updated_at']
    pass

admin.site.register(CustomUser, CustomUserAdmin)
