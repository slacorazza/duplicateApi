from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Invoice
from .serializers import InvoiceSerializer
from rest_framework.pagination import PageNumberPagination
from django.db.models import Sum

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
                'total_similar_invoices': total_invoices - total_groups,
                'total_open_similar_invoices': total_open_invoices - total_open_groups,
                'total_value_of_similar_invoices': total_value,
                'total_value_of_open_similar_invoices': total_open_value
            })
        except Exception as e:
            print(f"Error processing request: {e}")
            return Response({"error": str(e)}, status=500)
        
class Metadata(APIView):
    def get (self, request, format=None):
        try:
            reference_list = Invoice.objects.values_list('reference', flat=True).distinct()
            vendor_list = Invoice.objects.values_list('vendor', flat=True).distinct()
            pattern_list = Invoice.objects.values_list('pattern', flat=True).distinct()
            date_list = Invoice.objects.values_list('date', flat=True).distinct()
            return Response({
                'reference_values': reference_list,
                'vendor_values': vendor_list,
                'pattern_values': pattern_list,
                'date_values': date_list
            })
           
        except Exception as e:
            print(f"Error processing request: {e}")
            return Response({"error": str(e)}, status=500)
        
class GroupList(APIView):
    def get(self, request, format=None):
        try:
            group_list = Invoice.objects.values_list('group_id', flat=True).distinct()
            group_data = []

            for group_id in group_list:
                group_invoices = Invoice.objects.filter(group_id=group_id)
                group_value = group_invoices.aggregate(Sum('value'))['value__sum']
                first_invoice_value = group_invoices.first().value if group_invoices.exists() else 0
                group_value -= first_invoice_value
                group_invoices_count = group_invoices.count()
                serialized_invoices = InvoiceSerializer(group_invoices, many=True).data

                group_data.append({
                    'group_id': group_id,
                    'amount_overpaid': group_value,
                    'itemCount': group_invoices_count,
                    'date': group_invoices.order_by('date').first().date if group_invoices.exists() else None,
                    'region': group_invoices.first().region if group_invoices.exists() else None,
                    'pattern': group_invoices.first().pattern if group_invoices.exists() else None,
                    'open': group_invoices.first().open if group_invoices.exists() else None,
                    'confidence': group_invoices.first().confidence if group_invoices.exists() else None,
                    'items': serialized_invoices,
                })

            paginator = PageNumberPagination()
            page_size = request.query_params.get('page_size', paginator.page_size)
            if not page_size:
                page_size = 20
            paginator.page_size = page_size
            paginated_group_data = paginator.paginate_queryset(group_data, request)
            return paginator.get_paginated_response(paginated_group_data)

        except Exception as e:
            print(f"Error processing request: {e}")
            return Response({"error": str(e)}, status=500)
