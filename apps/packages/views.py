from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Package
from .serializers import PackageSerializer
from apps.users.permissions import IsSuperAdmin, get_tenant_id


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def list_packages(request):
    tenant_id = get_tenant_id(request)
    if not tenant_id:
        return Response({"error": "tenant_id required"}, status=status.HTTP_400_BAD_REQUEST)

    packages = Package.objects.filter(tenant_id=tenant_id).order_by("-created_at")
    return Response(PackageSerializer(packages, many=True).data)


@api_view(["POST"])
@permission_classes([IsAuthenticated, IsSuperAdmin])
def create_package(request):
    tenant_id = request.data.get("tenant_id") or get_tenant_id(request)
    if not tenant_id:
        return Response({"error": "tenant_id required"}, status=status.HTTP_400_BAD_REQUEST)

    package = Package.objects.create(
        tenant_id=tenant_id,
        total=request.data.get("total_credits", request.data.get("total", 0)),
        type=request.data.get("type", "base"),
        expires_at=request.data.get("expires_at"),
    )
    return Response(PackageSerializer(package).data, status=status.HTTP_201_CREATED)


@api_view(["POST"])
@permission_classes([IsAuthenticated, IsSuperAdmin])
def add_excess(request, package_id):
    try:
        package = Package.objects.get(pk=package_id)
    except Package.DoesNotExist:
        return Response({"error": "Package not found"}, status=status.HTTP_404_NOT_FOUND)

    credits = int(request.data.get("credits", 0))
    package.total += credits
    package.save()
    return Response(PackageSerializer(package).data)
