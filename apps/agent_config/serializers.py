from rest_framework import serializers
from .models import AgentConfig


class AgentConfigSerializer(serializers.ModelSerializer):
    tenant_id = serializers.UUIDField(source="tenant_id", read_only=True)
    companyInfo = serializers.CharField(source="company_info", required=False, allow_blank=True)
    qualificationCriteria = serializers.JSONField(source="qualification_criteria", required=False)
    toneOfVoice = serializers.CharField(source="tone_of_voice", required=False)
    reEngagementConfig = serializers.SerializerMethodField()

    class Meta:
        model = AgentConfig
        fields = [
            "tenant_id",
            "companyInfo",
            "icp",
            "qualificationCriteria",
            "toneOfVoice",
            "reEngagementConfig",
        ]

    def get_reEngagementConfig(self, obj):
        return {
            "enabled": obj.re_engagement_enabled,
            "delayHours": obj.re_engagement_delay_hours,
            "message": obj.re_engagement_message,
        }
