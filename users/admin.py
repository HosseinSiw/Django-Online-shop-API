from django.contrib import admin
from .models import User, Profile


class UserAdmin(admin.ModelAdmin):
    search_fields = ('username', 'email', "is_verified", 'is_staff', 'is_superuser')
    list_display = ('username', 'email', "is_verified", 'is_staff', 'is_superuser')
    list_filter = ('is_active', 'is_superuser', 'is_staff',)
    ordering = ('email',)
    filter_horizontal = ()
    fieldsets = (
        ("Personal", {"fields": ('username', "email", "password")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_verified", "is_superuser")}),
        ('Dates', {"fields": ("last_login",)}),
    )
    add_fieldsets = (
        ("Personal Info", {"fields": ('username', 'email', 'password1', 'password2')}),
        ("Permissions",  {'fields': ("is_active", "is_staff", "is_superuser", "is_verified")},)
    )


admin.site.register(User, UserAdmin)
admin.site.register(Profile)