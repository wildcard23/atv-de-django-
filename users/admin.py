from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomAdminUserCreationForm, CustomUserChangeForm
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    form = CustomUserChangeForm
    add_form = CustomAdminUserCreationForm
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Dados de acesso', {'fields': ('email',)}),
    )
    list_display = ('username', 'email', 'is_staff', 'is_active')
