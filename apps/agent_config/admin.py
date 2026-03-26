from django.contrib import admin

from .models import AgentConfig


@admin.register(AgentConfig)
class AgentConfigAdmin(admin.ModelAdmin):
    list_display = (
        "tenant",
        "tone_of_voice",
        "re_engagement_enabled",
        "re_engagement_delay_hours",
        "created_at",
        "updated_at",
    )
    list_filter = ("tone_of_voice", "re_engagement_enabled", "created_at", "updated_at")
    search_fields = ("tenant__name",)
    autocomplete_fields = ("tenant",)
    ordering = ("-updated_at",)
