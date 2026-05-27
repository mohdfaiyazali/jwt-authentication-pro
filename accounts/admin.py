from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):

    model = User

    list_display = (
        'id',
        'username',
        'email',
        'role',
        'is_staff',
        'is_superuser',
    )

    fieldsets = UserAdmin.fieldsets + (
        (
            'Custom Fields',
            {
                'fields': ('role',)
            }
        ),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            'Custom Fields',
            {
                'fields': ('role',)
            }
        ),
    )