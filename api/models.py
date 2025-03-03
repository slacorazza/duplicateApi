from django.db import models
from .constants import PATTERN_CHOICES

class Invoice(models.Model):
    """
    Model representing an invoice.

    Attributes:
        reference (str): The unique reference for the invoice.
        date (datetime): The date of the invoice.
        value (decimal): The value of the invoice.
        vendor (str): The name of the vendor without code.
        pattern (str): The pattern type of the invoice.
        open (bool): The status of the invoice, can be open or closed.
        group_id (str): The group ID associated with the invoice.
        confidence (str): The confidence level of the invoice.
        Region (str): The region associated with the invoice.
        Description (str): The description of the invoice.
        Payment_Method (str): The payment method for the invoice.
        Special_Instructions (str): Any special instructions for the invoice.
    """
    reference = models.CharField(max_length=50)
    date = models.DateTimeField(null=True, blank=True)
    value = models.DecimalField(max_digits=10, decimal_places=2)
    vendor = models.CharField(max_length=50)
    pattern = models.CharField(max_length=50, choices=PATTERN_CHOICES)
    open = models.BooleanField(default=True)
    group_id = models.CharField(max_length=50)
    confidence = models.CharField(max_length=6)
    Region = models.CharField(max_length=50, default='North')
    Description = models.CharField(max_length=250, default='No description')
    Payment_Method = models.CharField(max_length=50, default='Credit Card')
    Special_Instructions = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"Invoice {self.reference} from {self.vendor} on {self.date}"