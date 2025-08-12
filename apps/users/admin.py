from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, OTPVerification
from django.utils.translation import gettext_lazy as _

class UserAdmin(BaseUserAdmin):
    model = User
    list_display = ("phone", "is_admin", "phone_verified")
    search_fields = ("phone",)
    ordering = ("phone",)
    list_filter = ("is_admin", "is_superuser", "phone_verified")  # <- override here

    fieldsets = (
        (None, {"fields": ("phone", "password")}),
        (_("Permissions"), {"fields": ("is_admin", "phone_verified", "is_superuser", "groups", "user_permissions")}),
        (_("Important dates"), {"fields": ("last_login",)}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("phone", "password1", "password2"),
        }),
    )

admin.site.register(User, UserAdmin)
admin.site.register(OTPVerification)
