from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import AgentConfig
from .serializers import AgentConfigSerializer
from apps.users.permissions import IsTenantAdminOrAbove, get_tenant_id


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_agent_config(request):
    tenant_id = get_tenant_id(request)
    if not tenant_id:
        return Response({"error": "tenant_id required"}, status=status.HTTP_400_BAD_REQUEST)

    config, _ = AgentConfig.objects.get_or_create(tenant_id=tenant_id)
    return Response(AgentConfigSerializer(config).data)


@api_view(["PUT", "PATCH"])
@permission_classes([IsAuthenticated, IsTenantAdminOrAbove])
def update_agent_config(request):
    tenant_id = get_tenant_id(request)
    if not tenant_id:
        return Response({"error": "tenant_id required"}, status=status.HTTP_400_BAD_REQUEST)

    config, _ = AgentConfig.objects.get_or_create(tenant_id=tenant_id)
    data = request.data

    if "companyInfo" in data:
        config.company_info = data["companyInfo"]
    if "icp" in data:
        config.icp = data["icp"]
    if "toneOfVoice" in data:
        config.tone_of_voice = data["toneOfVoice"]
    if "qualificationCriteria" in data:
        config.qualification_criteria = data["qualificationCriteria"]
    if "reEngagementConfig" in data:
        re = data["reEngagementConfig"]
        if "enabled" in re:
            config.re_engagement_enabled = re["enabled"]
        if "delayHours" in re:
            config.re_engagement_delay_hours = re["delayHours"]
        if "message" in re:
            config.re_engagement_message = re["message"]

    config.save()
    return Response(AgentConfigSerializer(config).data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_qualification_criteria(request):
    tenant_id = get_tenant_id(request)
    if not tenant_id:
        return Response({"error": "tenant_id required"}, status=status.HTTP_400_BAD_REQUEST)

    config, _ = AgentConfig.objects.get_or_create(tenant_id=tenant_id)
    return Response({"questions": config.qualification_criteria})


@api_view(["PUT"])
@permission_classes([IsAuthenticated, IsTenantAdminOrAbove])
def update_qualification_criteria(request):
    tenant_id = get_tenant_id(request)
    if not tenant_id:
        return Response({"error": "tenant_id required"}, status=status.HTTP_400_BAD_REQUEST)

    config, _ = AgentConfig.objects.get_or_create(tenant_id=tenant_id)
    config.qualification_criteria = request.data.get("questions", [])
    config.save()
    return Response({"success": True})
