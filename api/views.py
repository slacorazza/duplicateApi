from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Invoice
from .serializers import InvoiceSerializer
from rest_framework.pagination import PageNumberPagination
from django.db.models import Sum
import logging

class InvoiceList(APIView):
    """
    API view to retrieve a list of invoices with optional filters.

    Filters:
        - reference: Filter by invoice references (multiple values allowed)
        - vendor: Filter by vendor names (multiple values allowed)
        - pattern: Filter by pattern types (multiple values allowed)
        - open: Filter by open status (true/false)
        - group: Filter by group ID
        - start_date: Filter by start date (inclusive)
        - end_date: Filter by end date (inclusive)
        - random: Randomize the order of the results (true/false)
    """
    def get(self, request, format=None):
        try:
            references = request.query_params.getlist('reference')
            vendors = request.query_params.getlist('vendor')
            patterns = request.query_params.getlist('pattern')
            open = request.query_params.get('open')
            group = request.query_params.get('group_id')
            start_date = request.query_params.get('start_date')
            end_date = request.query_params.get('end_date')
            random = request.query_params.get('random')

            print(f"Received request with filters: references={references}, vendors={vendors}, patterns={patterns}, open={open}, group={group}, start_date={start_date}, end_date={end_date}, random={random}")

            invoices = Invoice.objects.all()
            print(f"Found {invoices.count()} invoices")
            if references:
                invoices = invoices.filter(reference__in=references)
            if vendors:
                invoices = invoices.filter(vendor__in=vendors)
            if patterns:
                invoices = invoices.filter(pattern__in=patterns)
            if open:
                invoices = invoices.filter(open=open.lower() == 'true')
            if group:
                invoices = invoices.filter(group_id=group)
            if start_date:
                invoices = invoices.filter(date__gte=start_date)
            if end_date:
                invoices = invoices.filter(date__lte=end_date)
            if random and random.lower() == 'true':
                invoices = invoices.order_by('?')

            paginator = PageNumberPagination()
            paginated_invoices = paginator.paginate_queryset(invoices, request)
            serializer = InvoiceSerializer(paginated_invoices, many=True)
            return paginator.get_paginated_response(serializer.data)
        except Exception as e:
            print(f"Error processing request: {e}")
            return Response({"error": str(e)}, status=500)

class KPIsList(APIView):
    """
    API view to retrieve KPIs.

    Returns:
        - Total similar invoices
        - Total open similar invoices
        - Total value of similar invoices
        - Total value of open similar invoices
    """
    def get(self, request, format=None):
        try:
            total_invoices = Invoice.objects.count()
            total_groups = Invoice.objects.values('group_id').distinct().count()
            total_open_invoices = Invoice.objects.filter(open=True).count()
            total_open_groups = Invoice.objects.filter(open=True).values('group_id').distinct().count()
            total_value = Invoice.objects.aggregate(Sum('value'))['value__sum']
            total_open_value = Invoice.objects.filter(open=True).aggregate(Sum('value'))['value__sum']
            return Response({
                'Total similar invoices': total_invoices - total_groups,
                'Total open similar invoices': total_open_invoices - total_open_groups,
                'Total value of similar invoices': total_value,
                'Total value of open similar invoices': total_open_value
            })
        except Exception as e:
            print(f"Error processing request: {e}")
            return Response({"error": str(e)}, status=500)
        
