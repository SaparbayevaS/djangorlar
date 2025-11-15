from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email', 'username', 'first_name', 'last_name', 'phone', 'city', 'country', 'department', 'role', 'birth_date', 'salary', 'is_staff', 'is_active'
                    )
    list_filter = ('is_staff', 'is_active', 'role', 'department', 'city', 'country')
    search_fields = ('email', 'username', 'first_name', 'last_name', 'phone', 'city', 'country')
    