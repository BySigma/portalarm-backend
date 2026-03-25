from rest_framework.permissions import BasePermission


class IsSuperAdmin(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and hasattr(request.user, "profile")
            and request.user.profile.role == "super_admin"
        )


class IsTenantAdminOrAbove(BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        if not hasattr(request.user, "profile"):
            return False
        return request.user.profile.role in ("super_admin", "tenant_admin")


def get_tenant_id(request):
    """Return the tenant_id for the current user, or None for super_admin."""
    if not hasattr(request.user, "profile"):
        return None
    profile = request.user.profile
    if profile.role == "super_admin":
        return request.query_params.get("tenant_id") or request.data.get("tenant_id")
    return str(profile.tenant_id) if profile.tenant_id else None
