from django.urls import path
from . import views

"""
URL configuration for the API.

This module defines the URL patterns for the API endpoints, mapping them to the corresponding views.

Endpoints:
    - /invoices/ : Retrieve a list of invoices (InvoiceList view)
    - /kpis/ : Retrieve KPIs (KPIsList view)
    - /metadata/ : Retrieve metadata (Metadata view)
    - /groups/ : Retrieve a list of groups (GroupList view)
"""

urlpatterns = [
    path("invoices/", views.InvoiceList.as_view(), name="invoice-list"),
    path("kpis/", views.KPIsList.as_view(), name="kpis-list"),
    path("metadata/", views.Metadata.as_view(), name="metadata-list"),
    path("groups/", views.GroupList.as_view(), name="group-list"),
    
]