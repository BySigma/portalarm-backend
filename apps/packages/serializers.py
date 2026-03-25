from rest_framework import serializers
from .models import Package


class PackageSerializer(serializers.ModelSerializer):
    tenantId = serializers.UUIDField(source="tenant_id", read_only=True)
    remaining = serializers.SerializerMethodField()
    expiresAt = serializers.DateTimeField(source="expires_at", allow_null=True, required=False)

    class Meta:
        model = Package
        fields = ["id", "tenantId", "total", "used", "remaining", "type", "expiresAt"]

    def get_remaining(self, obj):
        return obj.remaining
