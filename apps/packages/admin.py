from django.contrib import admin

from .models import Package


@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    list_display = ("tenant", "type", "total", "used", "remaining", "expires_at", "created_at")
    list_filter = ("type", "expires_at", "created_at")
    search_fields = ("tenant__name",)
    autocomplete_fields = ("tenant",)
    ordering = ("-created_at",)
