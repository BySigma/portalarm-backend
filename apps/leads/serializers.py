from rest_framework import serializers
from .models import Lead


class LeadSerializer(serializers.ModelSerializer):
    tenant_id = serializers.UUIDField(source="tenant_id", read_only=True)
    lastContact = serializers.DateTimeField(source="last_contact", allow_null=True, required=False)
    createdAt = serializers.DateTimeField(source="created_at", read_only=True)
    disqualificationReason = serializers.CharField(
        source="disqualification_reason", required=False, allow_blank=True, default=""
    )

    class Meta:
        model = Lead
        fields = [
            "id",
            "tenant_id",
            "name",
            "phone",
            "channel",
            "status",
            "interactions",
            "lastContact",
            "createdAt",
            "disqualificationReason",
        ]

    def create(self, validated_data):
        return Lead.objects.create(**validated_data)
