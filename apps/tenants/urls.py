from django.urls import path
from . import views

urlpatterns = [
    path("admin/tenants/", views.list_tenants, name="list-tenants"),
    path("admin/tenants/create/", views.create_tenant, name="create-tenant"),
    path("admin/tenants/<uuid:tenant_id>/", views.update_tenant, name="update-tenant"),
    path("admin/tenants/<uuid:tenant_id>/suspend/", views.suspend_tenant, name="suspend-tenant"),
]
