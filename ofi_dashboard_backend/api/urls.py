from django.urls import path
from . import views

urlpatterns = [
    path("invoices/", views.InvoiceList.as_view(), name="invoice-list"),
    path("kpis/", views.KPIsList.as_view(), name="kpis-list"),
]