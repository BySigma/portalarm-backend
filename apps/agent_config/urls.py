from django.urls import path
from . import views

urlpatterns = [
    path("agent-config/", views.get_agent_config, name="get-agent-config"),
    path("agent-config/update/", views.update_agent_config, name="update-agent-config"),
    path("agent-config/qualification-criteria/", views.get_qualification_criteria, name="get-qualification-criteria"),
    path("agent-config/qualification-criteria/update/", views.update_qualification_criteria, name="update-qualification-criteria"),
]
