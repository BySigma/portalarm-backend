from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()
    tenant_id = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ["id", "name", "email", "role", "tenant_id"]

    def get_name(self, obj):
        return obj.name

    def get_email(self, obj):
        return obj.email

    def get_tenant_id(self, obj):
        return str(obj.tenant_id) if obj.tenant_id else None


class MeSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    role = serializers.SerializerMethodField()
    tenant_id = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["id", "username", "email", "name", "role", "tenant_id"]

    def get_id(self, obj):
        return str(obj.profile.id) if hasattr(obj, "profile") else str(obj.id)

    def get_name(self, obj):
        return obj.get_full_name() or obj.username

    def get_role(self, obj):
        return obj.profile.role if hasattr(obj, "profile") else "member"

    def get_tenant_id(self, obj):
        if hasattr(obj, "profile") and obj.profile.tenant_id:
            return str(obj.profile.tenant_id)
        return None
