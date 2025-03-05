from django.urls import path
from . import views


urlpatterns = [
    path("initial_data/", views.InitialData.as_view(), name="initial-data"),
    path("ai_assistant/", views.AiAssistant.as_view(), name="ai-assistant"),
]