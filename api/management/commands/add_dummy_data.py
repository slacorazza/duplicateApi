import csv
from django.core.management.base import BaseCommand
from api.models import Invoice
from django.utils.dateparse import parse_datetime
from django.conf import settings
import os
from decimal import Decimal
import random
from datetime import datetime, timedelta

class Command(BaseCommand):
    """
    Django management command to add data to the database from a CSV file.
    """
    help = 'Add data to the database from CSV file'

    def similar_text(self, text):
        """
        Return a similar text based on the input text.
        """
        case = random.choice([0, 1, 2])
        if case == 0:
            return self.delete_random_char(text)
        elif case == 1:
            return self.duplicate_random_char(text)
        else:
            return self.replace_random_char(text)


    def delete_random_char(self, text):
        """
        Delete a random character from the input text.
        """
        if len(text) > 0:
            index = random.randint(0, len(text) - 1)
            return text[:index] + text[index + 1:]
        return text
    
    def duplicate_random_char(self, text):
        """
        Duplicate a random character from the input text.
        """
        if len(text) > 0:
            index = random.randint(0, len(text) - 1)
            return text[:index] + text[index] + text[index:]
        return text
    
    def replace_random_char(self, text):
        """
        Replace a random character from the input text.
        """
        if len(text) > 0:
            index = random.randint(0, len(text) - 1)
            return text[:index] + chr(random.randint(97, 122)) + text[index + 1:]
        return text
    
    def handle(self, *args, **kwargs):
        """
        Handle the command to add data to the database from the CSV file.
        """
        # Path to the CSV file
        csv_file_path = os.path.join(settings.BASE_DIR, 'api', 'data', 'DummyData.csv')

        # Read the CSV file
        with open(csv_file_path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            counter = 0

            for  row in reader:
                duplicate_n = random.randint(0, 5)
                invoice_ref = 'INV-' + str(counter)
                date_str = row['Earliest Due Date']
                if date_str == '':
                    date = datetime(2024, 1, 1) + timedelta(days=counter)
                else:
                    date = parse_datetime(date_str)
                    # Convert date from MM/DD/YYYY to YYYY-MM-DD format
                    try:
                        date = datetime.strptime(date_str, '%m/%d/%Y').strftime('%Y-%m-%d')
                    except ValueError:
                        raise ValueError(f"Invalid date format: {date_str} in row {counter}")
                value = Decimal(row['Group Value'])
                vendor = row['Vendor'].split(' - ', 1)[-1]
                pattern = row['Group Pattern']
                open_ = random.choice([True, False])
                group_id = row['Group UUID']
                confidense = row['Confidence'].strip()
                region = random.choice(['North', 'South', 'East', 'West'])
                description = row['Description']
                payment_method = random.choice(['Credit Card', 'Bank Transfer', 'PayPal', 'Cash'])
                special_instructions = row['Special Intructions']


                if 'Open' in row['Group Contains']:
                    open_ = True
                else:
                    open_ = False

                Invoice.objects.create(reference=invoice_ref, date=date, value=value, vendor=vendor, pattern=pattern, open=open_, group_id=group_id, confidence=confidense, Region=region, Description=description, Payment_Method=payment_method, Special_Instructions=special_instructions)
                
                counter += 1
                
                for i in range(1, duplicate_n):
                    invoice_ref = 'INV-' + str(counter)
                    if pattern == 'Similar Value':
                        value = str(float(value) + random.randint(-30, 30))
                    elif pattern == 'Similar Vendor':
                        vendor = self.similar_text(vendor)
                    elif pattern == 'Similar Date':
                        date = date + timedelta(days=i)
                    elif pattern == 'Similar Reference':
                        invoice_ref = self.similar_text(invoice_ref)
                    elif pattern == 'Similar Description':
                        description = self.similar_text(description)
                    

                    Invoice.objects.create(reference=invoice_ref, date=date, value=value, vendor=vendor, pattern=pattern, open=open_, group_id=group_id, confidence=confidense, Region=region, Description=description, Payment_Method=payment_method, Special_Instructions=special_instructions)

        self.stdout.write(self.style.SUCCESS('Data added successfully'))