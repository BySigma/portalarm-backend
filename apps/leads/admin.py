from django.contrib import admin

from .models import Lead


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "phone",
        "tenant",
        "status",
        "channel",
        "interactions",
        "last_contact",
        "created_at",
    )
    list_filter = ("status", "channel", "tenant", "created_at", "last_contact")
    search_fields = ("name", "phone", "tenant__name")
    autocomplete_fields = ("tenant",)
    ordering = ("-created_at",)
