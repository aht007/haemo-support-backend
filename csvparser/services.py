"""
CSV Parser Service
"""
from accounts.serializers import RegisterSerializer
import csv
from collections import defaultdict
from django.core.exceptions import ValidationError


class Csv_Parser:
    """
    CSV Parser Class for adding bulk donor users
    """
    required_columns = ['username', 'email', 'password',
                        'date_of_birth', 'phone_number', 'blood_group']

    def __init__(self, file):
        self.file = file
        self.error_messages = defaultdict(list)

    def add_error(self, message, row=0):
        """
        Add an error message to error_messages list
        """
        self.error_messages[message].append(row)

    def validate_file(self, file_reader):
        """
        Validates if required fields are present in given file
        """
        if self.required_columns:
            for field in self.required_columns:
                if field not in file_reader.fieldnames:
                    raise ValidationError(
                        f"Missing column: {field}")

    # pylint: disable=inconsistent-return-statements

    def read_file(self):
        """
        Create a CSV reader and validate the file.
        """
        data_list = []
        try:
            with open(self.file, 'r', encoding="UTF-8") as openedFile:
                reader = csv.DictReader(openedFile)
                self.validate_file(reader)
                for row in reader:
                    valid_row = self.validate_row(row)
                    if valid_row:
                        data_list.append(row)

            return data_list

        except ValidationError as exc:
            self.add_error(str(exc))
            return []

    def validate_row(self, row):
        """
        Validate the fields in the row.
        if valid return true else add error to error variable and return false
        """
        serializer = RegisterSerializer(data=row)
        if serializer.is_valid():
            return True
        else:
            return False
