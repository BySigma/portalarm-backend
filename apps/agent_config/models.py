import uuid
from django.db import models


class AgentConfig(models.Model):
    TONE_CHOICES = [
        ("professional", "Professional"),
        ("friendly", "Friendly"),
        ("casual", "Casual"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tenant = models.OneToOneField(
        "tenants.Tenant",
        on_delete=models.CASCADE,
        related_name="agent_config",
    )
    company_info = models.TextField(blank=True, default="")
    icp = models.TextField(blank=True, default="")
    qualification_criteria = models.JSONField(default=list)
    tone_of_voice = models.CharField(max_length=20, choices=TONE_CHOICES, default="professional")
    re_engagement_enabled = models.BooleanField(default=False)
    re_engagement_delay_hours = models.IntegerField(default=24)
    re_engagement_message = models.TextField(blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "agent_config"

    def __str__(self):
        return f"Agent config for {self.tenant_id}"
