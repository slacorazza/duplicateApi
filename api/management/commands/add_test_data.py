import csv
from django.core.management.base import BaseCommand
from django.conf import settings
import os
import random
from datetime import datetime, timedelta

class Command(BaseCommand):
    help = 'Read data from a CSV file and write data to another CSV file'


    def get_data(self):
                # Path to the input CSV file
        input_csv_file_path = os.path.join(settings.BASE_DIR, 'api', 'data', 'TestData.csv')
        
       

        # Read data from the input CSV file
        with open(input_csv_file_path, newline='', encoding='utf-8-sig') as input_csvfile:
            reader = csv.DictReader(input_csvfile)
            data = [row for row in reader]
        return data
    

    def write_data(self, data):
         # Path to the output CSV file
        output_csv_file_path = os.path.join(settings.BASE_DIR, 'api', 'data', 'OutputData.csv')

        with open(output_csv_file_path, 'w', newline='', encoding='utf-8-sig') as output_csvfile:
            fieldnames = data[0].keys()
            writer = csv.DictWriter(output_csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
        self.stdout.write(self.style.SUCCESS('Data processed and written to output CSV file successfully'))

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
    

    def similar_text(self, confidence, text):
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
        

    def handle(self, *args, **kwargs):

        data = self.get_data()

        # Process the data (example: add a new field)
        new_data = []
        for row in data:

            row['Reference'] = 'Inv-' + str(random.randint(0, 9999))
            row['Region'] = random.choice(['North', 'South', 'East', 'West'])
            row['Payment Method'] = random.choice(['Credit Card', 'Bank Transfer', 'PayPal', 'Cash'])
            row['Earliest Due Date'] = (datetime(2025, 1, 1) + timedelta(days=random.randint(1, 100))).strftime('%Y-%m-%d')
            row['Vendor'] = row['Vendor'].split(' - ', 1)[-1]
            
            duplicate_n = random.randint(1, 5)
            unique = row['Group Pattern'] == 'unique'
            group_pattern = row['Group Pattern']
            confidence = row['Confidence']
            if not unique:
                for i in range(duplicate_n):
                    new_row = row.copy()
                    if group_pattern == 'similar special_instructions':
                        new_row['Special Intructions'] = self.similar_text(confidence, new_row['Special Intructions'])
                    elif group_pattern == 'similar reference':
                        new_row['Reference'] = self.similar_text(confidence, new_row['Reference'])
                    elif group_pattern == 'similar date':
                        new_row['Earliest Due Date'] = self.similar_text(confidence, new_row['Earliest Due Date'])
                    elif group_pattern == 'similar value':
                        new_row['Group Value'] = self.similar_text(confidence, new_row['Group Value'])
                    elif group_pattern == 'similar vendor':
                        new_row['Vendor'] = self.similar_text(confidence, new_row['Vendor'])
                    elif group_pattern == 'similar region':
                        new_row['Region'] = self.similar_text(confidence, new_row['Region'])
                    elif group_pattern == 'similar description':
                        new_row['Description'] = self.similar_text(confidence, new_row['Description'])
                    elif group_pattern == 'similar payment_method':
                        new_row['Payment Method'] = self.similar_text(confidence, new_row['Payment Method'])


                    new_data.append(new_row)

        data.extend(new_data)
        self.write_data(data)


       
        