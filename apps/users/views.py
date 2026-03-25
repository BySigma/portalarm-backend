from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Profile
from .serializers import ProfileSerializer, MeSerializer
from .permissions import IsTenantAdminOrAbove, get_tenant_id


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def me(request):
    return Response(MeSerializer(request.user).data)


@api_view(["GET"])
@permission_classes([IsAuthenticated, IsTenantAdminOrAbove])
def list_users(request):
    tenant_id = get_tenant_id(request)
    if not tenant_id:
        return Response({"error": "tenant_id required"}, status=status.HTTP_400_BAD_REQUEST)

    profiles = Profile.objects.filter(tenant_id=tenant_id).select_related("user")
    return Response(ProfileSerializer(profiles, many=True).data)


@api_view(["POST"])
@permission_classes([IsAuthenticated, IsTenantAdminOrAbove])
def invite_user(request):
    email = request.data.get("email")
    role = request.data.get("role", "member")
    tenant_id = get_tenant_id(request)

    if not email or not tenant_id:
        return Response({"error": "email and tenant_id are required"}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(email=email).exists():
        return Response({"error": "User with this email already exists"}, status=status.HTTP_400_BAD_REQUEST)

    username = email.split("@")[0]
    base_username = username
    counter = 1
    while User.objects.filter(username=username).exists():
        username = f"{base_username}{counter}"
        counter += 1

    user = User.objects.create_user(username=username, email=email)
    Profile.objects.create(user=user, tenant_id=tenant_id, role=role)

    return Response({"success": True, "message": f"User {email} invited successfully"})


@api_view(["PUT", "PATCH"])
@permission_classes([IsAuthenticated, IsTenantAdminOrAbove])
def update_user(request, user_id):
    try:
        profile = Profile.objects.get(pk=user_id)
    except Profile.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    if "role" in request.data:
        profile.role = request.data["role"]
        profile.save()

    return Response(ProfileSerializer(profile).data)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated, IsTenantAdminOrAbove])
def delete_user(request, user_id):
    try:
        profile = Profile.objects.get(pk=user_id)
    except Profile.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    profile.user.delete()
    return Response({"success": True})
