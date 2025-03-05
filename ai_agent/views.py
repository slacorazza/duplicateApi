from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView


class InitialData(APIView):

    def get(self, request, format=None):
         return Response({
                'New Invoices': 23,
                'New Duplicate Invoices': 6,
                'Alert': 'The company Acme Corportion has 3 new invoices with a high confidence level of being duplicates. I recommend reviewing these invoices.',
            })