import uuid
from django.db import models


class Lead(models.Model):
    STATUS_CHOICES = [
        ("qualified", "Qualified"),
        ("in_progress", "In Progress"),
        ("forwarded", "Forwarded"),
        ("disqualified", "Disqualified"),
        ("reengagement", "Re-engagement"),
    ]

    CHANNEL_CHOICES = [
        ("WhatsApp", "WhatsApp"),
        ("Instagram", "Instagram"),
        ("Facebook", "Facebook"),
        ("Site", "Site"),
        ("Outros", "Outros"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tenant = models.ForeignKey(
        "tenants.Tenant",
        on_delete=models.CASCADE,
        related_name="leads",
    )
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=50)
    channel = models.CharField(max_length=20, choices=CHANNEL_CHOICES, default="WhatsApp")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="in_progress")
    interactions = models.IntegerField(default=0)
    last_contact = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    disqualification_reason = models.TextField(blank=True, default="")

    class Meta:
        db_table = "leads"
        unique_together = [("tenant", "phone")]

    def __str__(self):
        return f"{self.name} ({self.phone})"
