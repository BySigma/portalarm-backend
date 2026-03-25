from django.urls import path
from . import views

urlpatterns = [
    path("packages/", views.list_packages, name="list-packages"),
    path("packages/create/", views.create_package, name="create-package"),
    path("packages/<uuid:package_id>/add-excess/", views.add_excess, name="add-excess"),
]
