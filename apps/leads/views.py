from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Lead
from .serializers import LeadSerializer
from apps.users.permissions import get_tenant_id


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def list_leads(request):
    tenant_id = get_tenant_id(request)
    if not tenant_id:
        return Response({"error": "tenant_id required"}, status=status.HTTP_400_BAD_REQUEST)

    qs = Lead.objects.filter(tenant_id=tenant_id).order_by("-created_at")

    lead_status = request.query_params.get("status")
    if lead_status:
        qs = qs.filter(status=lead_status)

    channel = request.query_params.get("channel")
    if channel:
        qs = qs.filter(channel=channel)

    search = request.query_params.get("search")
    if search:
        qs = qs.filter(name__icontains=search) | qs.filter(phone__icontains=search)

    leads = list(qs)
    return Response({"leads": LeadSerializer(leads, many=True).data, "total": len(leads)})


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_lead(request):
    tenant_id = get_tenant_id(request)
    if not tenant_id:
        return Response({"error": "tenant_id required"}, status=status.HTTP_400_BAD_REQUEST)

    data = {**request.data, "tenant": tenant_id}
    serializer = LeadSerializer(data=request.data)
    if serializer.is_valid():
        lead = Lead.objects.create(
            tenant_id=tenant_id,
            name=serializer.validated_data["name"],
            phone=serializer.validated_data["phone"],
            channel=serializer.validated_data.get("channel", "WhatsApp"),
        )
        return Response(LeadSerializer(lead).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_lead(request, lead_id):
    tenant_id = get_tenant_id(request)
    try:
        lead = Lead.objects.get(pk=lead_id, tenant_id=tenant_id)
    except Lead.DoesNotExist:
        return Response({"error": "Lead not found"}, status=status.HTTP_404_NOT_FOUND)

    return Response(LeadSerializer(lead).data)


@api_view(["PUT", "PATCH"])
@permission_classes([IsAuthenticated])
def update_lead(request, lead_id):
    tenant_id = get_tenant_id(request)
    try:
        lead = Lead.objects.get(pk=lead_id, tenant_id=tenant_id)
    except Lead.DoesNotExist:
        return Response({"error": "Lead not found"}, status=status.HTTP_404_NOT_FOUND)

    data = request.data
    if "status" in data:
        lead.status = data["status"]
    if "interactions" in data:
        lead.interactions = data["interactions"]
    if "lastContact" in data:
        lead.last_contact = data["lastContact"]
    if "disqualificationReason" in data:
        lead.disqualification_reason = data["disqualificationReason"]
    lead.save()

    return Response(LeadSerializer(lead).data)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_lead(request, lead_id):
    tenant_id = get_tenant_id(request)
    try:
        lead = Lead.objects.get(pk=lead_id, tenant_id=tenant_id)
    except Lead.DoesNotExist:
        return Response({"error": "Lead not found"}, status=status.HTTP_404_NOT_FOUND)

    lead.delete()
    return Response({"success": True})
