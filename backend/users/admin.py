from django.contrib import admin
from .models import CustomUser
from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

# Register your models here.


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    list_display = [
        'username',
        'first_name',
        'last_name',
        'region',
        'city',
        'org_name',
    ]
    fieldsets = (
        *UserAdmin.fieldsets,
        (
            'Additional information',
            {
                'fields': (
                    'region',
                    'city',
                    'org_name',
                )
            }
        )
    )


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.unregister(Group)
