from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Invoice
from .serializers import InvoiceSerializer
from rest_framework.pagination import PageNumberPagination
from django.db.models import Sum
import logging
from openai import OpenAI

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
        
class AiAssistant(APIView):
    # Get the OpenAI API key from environment variables
    OPENAI_API_KEY = 'fffffffffff'

    conversation_history = [
                    {"role": "system", "content": "You are a helpful assistant called OfiA. You were designed by the company Ofiservices to help with duplicate invoice identification. Your main function is to give the user meaningful insights and advice about the invoices in the system."},
                    {"role": "system", "content": "Each invoice has this information: Group Pattern, Confidence, Company Code, Vendor, Group Value, Amount Overbooked, Group Contains, Earliest Due Date, Group UUID, Region, Description, Payment Method and Special Intructions."},
                    {"role": "system", "content": "Always give some advice or recommendation to the user."},
                    {"role": "system", "content": "When asked something you don't know, you make something up. You never say you dont know or that you cant access data. If asked with a specific number or data you return a random number which makes sense."},
                    {"role": "system", "content": "This is the list of vendors: Acme Corporation, Destec Office, Global Business, AluCast, Manhattan Corporation, State of California, Enigma, IOT Furniture, Pyramid Systems, WCB, Noe Food Company, Meyers Real Estate, GATORSA, Aztec Supplies, World Wide, CAFS Chemicals, CET New York"}, 
                    {"role": "system", "content": "Always start by introducing yourself"},
                    {"role": "system", "content": "The references of each invoices have this structure: INV-<number>"},
                    {"role": "system", "content": "These are the current KPI: Total similar invoices: 401 Total open similar invoices: 309 Total value of similar invoices: 1976659.459 Total value of open similar invoices: 1431130.88 "},
                    ]
    def message_openai(self, message):
        try:
            client = OpenAI(api_key=self.OPENAI_API_KEY)
            self.conversation_history.append({"role": "user", "content": message})
            completion = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=self.conversation_history
            )
            return completion.choices[0].message.content
        except Exception as e:
            print(f"Error communicating with OpenAI: {e}")
            return "Sorry, I couldn't process your request at the moment."

    def post(self, request, format=None):
        try:
            data = request.data
            message = data.get('message')
            response = self.message_openai(message)
            return Response({'response': response})
        except Exception as e:
            print(f"Error processing request: {e}")
            return Response({"error": str(e)}, status=500)