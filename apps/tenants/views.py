from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Tenant
from .serializers import TenantSerializer
from apps.users.permissions import IsSuperAdmin


@api_view(["GET"])
@permission_classes([IsAuthenticated, IsSuperAdmin])
def list_tenants(request):
    tenants = Tenant.objects.all().order_by("-created_at")
    return Response(TenantSerializer(tenants, many=True).data)


@api_view(["POST"])
@permission_classes([IsAuthenticated, IsSuperAdmin])
def create_tenant(request):
    serializer = TenantSerializer(data=request.data)
    if serializer.is_valid():
        tenant = serializer.save()
        return Response(TenantSerializer(tenant).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["PUT", "PATCH"])
@permission_classes([IsAuthenticated, IsSuperAdmin])
def update_tenant(request, tenant_id):
    try:
        tenant = Tenant.objects.get(pk=tenant_id)
    except Tenant.DoesNotExist:
        return Response({"error": "Tenant not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = TenantSerializer(tenant, data=request.data, partial=True)
    if serializer.is_valid():
        tenant = serializer.save()
        return Response(TenantSerializer(tenant).data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([IsAuthenticated, IsSuperAdmin])
def suspend_tenant(request, tenant_id):
    try:
        tenant = Tenant.objects.get(pk=tenant_id)
    except Tenant.DoesNotExist:
        return Response({"error": "Tenant not found"}, status=status.HTTP_404_NOT_FOUND)

    tenant.status = "suspended"
    tenant.save()
    return Response({"success": True})
