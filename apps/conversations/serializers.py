from rest_framework import serializers
from .models import Conversation


class ConversationSerializer(serializers.ModelSerializer):
    leadId = serializers.UUIDField(source="lead_id", read_only=True)

    class Meta:
        model = Conversation
        fields = ["leadId", "messages"]
