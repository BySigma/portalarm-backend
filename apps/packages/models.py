import uuid
from django.db import models


class Package(models.Model):
    TYPE_CHOICES = [
        ("base", "Base"),
        ("excess", "Excess"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tenant = models.ForeignKey(
        "tenants.Tenant",
        on_delete=models.CASCADE,
        related_name="packages",
    )
    total = models.IntegerField(default=0)
    used = models.IntegerField(default=0)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, default="base")
    expires_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "packages"

    @property
    def remaining(self):
        return max(0, self.total - self.used)

    def __str__(self):
        return f"{self.type} package for {self.tenant_id} ({self.remaining} remaining)"
