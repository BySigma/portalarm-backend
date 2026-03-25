from django.urls import path
from . import views

urlpatterns = [
    path("analytics/dashboard/", views.dashboard, name="dashboard"),
    path("analytics/reports/", views.reports, name="reports"),
    path("analytics/disqualified/", views.disqualified_leads, name="disqualified"),
]
