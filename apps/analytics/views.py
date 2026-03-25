from datetime import datetime, timedelta, timezone

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from django.db.models import Count

from apps.leads.models import Lead
from apps.packages.models import Package
from apps.users.permissions import get_tenant_id


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def dashboard(request):
    tenant_id = get_tenant_id(request)
    if not tenant_id:
        return Response({"error": "tenant_id required"}, status=status.HTTP_400_BAD_REQUEST)

    leads = Lead.objects.filter(tenant_id=tenant_id)
    total_leads = leads.count()
    attended = leads.exclude(status="in_progress").count()
    qualified = leads.filter(status="qualified").count()
    forwarded = leads.filter(status="forwarded").count()

    by_channel = list(
        leads.values("channel").annotate(count=Count("id")).order_by("-count")
    )
    by_status = list(
        leads.values("status").annotate(count=Count("id")).order_by("-count")
    )

    packages = Package.objects.filter(tenant_id=tenant_id).order_by("-created_at")
    base_pkg = packages.filter(type="base").first()
    balance = {
        "total": base_pkg.total if base_pkg else 0,
        "used": base_pkg.used if base_pkg else 0,
        "remaining": base_pkg.remaining if base_pkg else 0,
        "expiresAt": base_pkg.expires_at.isoformat() if base_pkg and base_pkg.expires_at else None,
    }

    return Response({
        "totalLeads": total_leads,
        "attendedBySdr": attended,
        "qualified": qualified,
        "forwarded": forwarded,
        "balance": balance,
        "byChannel": [{"channel": r["channel"], "count": r["count"]} for r in by_channel],
        "byStatus": [{"status": r["status"], "count": r["count"]} for r in by_status],
    })


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def reports(request):
    tenant_id = get_tenant_id(request)
    if not tenant_id:
        return Response({"error": "tenant_id required"}, status=status.HTTP_400_BAD_REQUEST)

    period = request.query_params.get("period", "30d")
    days = {"7d": 7, "30d": 30, "90d": 90}.get(period, 30)

    now = datetime.now(timezone.utc)
    start = now - timedelta(days=days)

    leads = Lead.objects.filter(tenant_id=tenant_id, created_at__gte=start)

    daily_data = {}
    for lead in leads:
        day = lead.created_at.date().isoformat()
        if day not in daily_data:
            daily_data[day] = {"date": day, "received": 0, "qualified": 0}
        daily_data[day]["received"] += 1
        if lead.status == "qualified":
            daily_data[day]["qualified"] += 1

    result = sorted(daily_data.values(), key=lambda x: x["date"])
    return Response(result)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def disqualified_leads(request):
    tenant_id = get_tenant_id(request)
    if not tenant_id:
        return Response({"error": "tenant_id required"}, status=status.HTTP_400_BAD_REQUEST)

    from apps.leads.serializers import LeadSerializer
    leads = Lead.objects.filter(tenant_id=tenant_id, status="disqualified").order_by("-created_at")
    return Response(LeadSerializer(leads, many=True).data)
