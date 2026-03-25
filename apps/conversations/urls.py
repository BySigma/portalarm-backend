from django.urls import path
from . import views

urlpatterns = [
    path("conversations/", views.list_conversations, name="list-conversations"),
    path("conversations/<uuid:lead_id>/", views.get_conversation, name="get-conversation"),
    path("conversations/<uuid:lead_id>/messages/", views.add_message, name="add-message"),
]
