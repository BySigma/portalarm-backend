from django.urls import path
from . import views

urlpatterns = [
    path("leads/", views.list_leads, name="list-leads"),
    path("leads/create/", views.create_lead, name="create-lead"),
    path("leads/<uuid:lead_id>/", views.get_lead, name="get-lead"),
    path("leads/<uuid:lead_id>/update/", views.update_lead, name="update-lead"),
    path("leads/<uuid:lead_id>/delete/", views.delete_lead, name="delete-lead"),
]
