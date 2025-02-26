from rest_framework import serializers
from .models import Invoice


## Serializer are used to convert complex data types, such as querysets and model instances, to native Python datatypes that can then be easily rendered into JSON, XML or other content types.

class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = 'reference', 'date', 'value', 'vendor', 'pattern', 'open', 'group_id'