from haemosupport.settings import DATA_FILE
from accounts.serializers import RegisterSerializer
from django.core.management.base import BaseCommand
from accounts.models import BloodGroupTypes
import csv
import json
class Command(BaseCommand):
    help = 'Seeds the Database'
    
    def handle(self, *args, **options):
        try:
            with open(DATA_FILE) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                line_count = 0
                for row in csv_reader:
                    if line_count == 0:
                        print(f'Column names are {", ".join(row)}')
                        line_count += 1
                    else:
                        data = {}
                        data['username'] = row[0]
                        data['password'] = row[1]
                        data['email'] = row[2]
                        data['date_of_birth'] = row[3]
                        data['phone_number'] = row[4]
                        data['blood_group'] = row[5]
                        data['is_admin'] = row[6]
                        serialaizer = RegisterSerializer(data=data)
                        serialaizer.is_valid(raise_exception=True)
                        serialaizer.save()
        except(OSError):
            print("Could not Open CSV FILE")
        except (FileNotFoundError):
            print("CSV FILE NOT FOUND")
        except Exception as err:
            print(f"Unexpected error :",repr(err))
