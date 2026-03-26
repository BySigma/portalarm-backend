from django.contrib import admin

from .models import Conversation


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ("lead", "created_at", "updated_at")
    search_fields = ("lead__name", "lead__phone", "lead__tenant__name")
    list_filter = ("created_at", "updated_at")
    autocomplete_fields = ("lead",)
    ordering = ("-updated_at",)
