from django.db import models
from .constants import PATTERN_CHOICES


class Invoice(models.Model):

    reference = models.CharField(max_length=50, primary_key=True)
    date = models.DateTimeField(null=True,blank=True)
    value = models.DecimalField(max_digits=10, decimal_places=2)
    vendor = models.CharField(max_length=50)
    pattern = models.CharField(max_length=50, choices=PATTERN_CHOICES)
    open = models.BooleanField(default=True)
    group_id = models.CharField(max_length=50)
    confidence = models.CharField(max_length=6, default='High')

    def __str__(self):
        return f"Invoice {self.reference} from {self.vendor} on {self.date}"