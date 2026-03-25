import uuid
from datetime import datetime, timezone

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Conversation
from .serializers import ConversationSerializer
from apps.leads.models import Lead
from apps.users.permissions import get_tenant_id


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_conversation(request, lead_id):
    tenant_id = get_tenant_id(request)
    try:
        lead = Lead.objects.get(pk=lead_id, tenant_id=tenant_id)
    except Lead.DoesNotExist:
        return Response({"error": "Lead not found"}, status=status.HTTP_404_NOT_FOUND)

    conversation, _ = Conversation.objects.get_or_create(lead=lead, defaults={"messages": []})
    return Response(ConversationSerializer(conversation).data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_message(request, lead_id):
    tenant_id = get_tenant_id(request)
    try:
        lead = Lead.objects.get(pk=lead_id, tenant_id=tenant_id)
    except Lead.DoesNotExist:
        return Response({"error": "Lead not found"}, status=status.HTTP_404_NOT_FOUND)

    conversation, _ = Conversation.objects.get_or_create(lead=lead, defaults={"messages": []})

    message = {
        "id": str(uuid.uuid4()),
        "role": request.data.get("role", "agent"),
        "content": request.data.get("content", ""),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "type": request.data.get("type", "text"),
    }
    if "mediaDescription" in request.data:
        message["mediaDescription"] = request.data["mediaDescription"]

    messages = list(conversation.messages)
    messages.append(message)
    conversation.messages = messages
    conversation.save()

    return Response(message, status=status.HTTP_201_CREATED)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def list_conversations(request):
    tenant_id = get_tenant_id(request)
    if not tenant_id:
        return Response({"error": "tenant_id required"}, status=status.HTTP_400_BAD_REQUEST)

    lead_qs = Lead.objects.filter(tenant_id=tenant_id)

    lead_status = request.query_params.get("status")
    if lead_status:
        lead_qs = lead_qs.filter(status=lead_status)

    conversations = Conversation.objects.filter(lead__in=lead_qs).select_related("lead")
    return Response(ConversationSerializer(conversations, many=True).data)
