from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .openai_client import get_openai_client


class Alerts(APIView):

    def get(self, request, format=None):
        return Response({
            'Alert': {
                'content': {
                    'new_invoices': 54,
                    'new_duplicate_invoices': 12,
                            },
                'type': "duplicated",
                'message': "The Canada Customs & Revenue Agency has 9 new invoices with a high confidence level of being duplicated. I recommend reviewing these invoices.",
                'UUID': '173cc4a2d7b9fc54dc35b9951cc28a7308b9b394bc09fc7544134a0f015d19e6',
                },
        })

class AiAssistant(APIView):
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
            client = get_openai_client()
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