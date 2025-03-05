from django.urls import path
from . import views


urlpatterns = [
    path("initial_data/", views.InitialData.as_view(), name="initial-data"),
]