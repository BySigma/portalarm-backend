from django.urls import path
from . import views

urlpatterns = [
    path("auth/me/", views.me, name="me"),
    path("users/", views.list_users, name="list-users"),
    path("users/invite/", views.invite_user, name="invite-user"),
    path("users/<uuid:user_id>/", views.update_user, name="update-user"),
    path("users/<uuid:user_id>/delete/", views.delete_user, name="delete-user"),
]
