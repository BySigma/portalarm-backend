from django.contrib import admin

from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "role", "tenant")
    list_filter = ("role", "tenant")
    search_fields = ("user__username", "user__first_name", "user__last_name", "user__email")
    autocomplete_fields = ("user", "tenant")
