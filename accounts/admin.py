# accounts/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User, UserProfile


class UserAdmin(BaseUserAdmin):
    ordering = ["email"]
    list_display = ["email", "username", "role", "is_staff", "is_active"]
    list_filter = ["role", "is_staff", "is_active"]

    fieldsets = (
        (None, {"fields": ("email", "username", "password")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "role", "groups", "user_permissions")}),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "username", "password1", "password2"),
        }),
    )

    search_fields = ("email", "username")


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "slug", "phone", "city", "area")
    search_fields = ("user__email", "user__username", "slug", "phone")
    readonly_fields = ("created_at", "updated_at")


admin.site.register(User, UserAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
