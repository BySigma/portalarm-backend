from rest_framework import serializers
from .models import Tenant


class TenantSerializer(serializers.ModelSerializer):
    wabaId = serializers.CharField(source="waba_id", required=False, default="")
    phoneNumber = serializers.CharField(source="phone_number", required=False, default="")
    createdAt = serializers.DateTimeField(source="created_at", read_only=True)

    class Meta:
        model = Tenant
        fields = ["id", "name", "wabaId", "phoneNumber", "status", "plan", "balance", "createdAt"]

    def create(self, validated_data):
        return Tenant.objects.create(**validated_data)
