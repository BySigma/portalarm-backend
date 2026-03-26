from django.contrib import admin

from .models import Tenant


@admin.register(Tenant)
class TenantAdmin(admin.ModelAdmin):
    list_display = ("name", "status", "plan", "balance", "phone_number", "created_at")
    list_filter = ("status", "plan", "created_at")
    search_fields = ("name", "waba_id", "phone_number")
    ordering = ("name",)
