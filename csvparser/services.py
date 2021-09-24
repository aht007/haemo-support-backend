"""
CSV Parser Service
"""
import csv
from accounts.serializers import RegisterSerializer



def decode_utf8(input_iterator):
    """
    Generator that decodes a utf-8 encoded
    input line by line
    """
    for line in input_iterator:
        yield line if isinstance(line, str) else line.decode('utf-8')


class Csv_Parser:
    """
    CSV Parser Class for adding bulk donor users
    """
    required_columns = ['username', 'email', 'password',
                        'date_of_birth', 'phone_number', 'blood_group']

    def __init__(self, file):
        self.file = file
        self.error_messages = []

    def add_error(self, message):
        """
        Add an error message to error_messages list
        """
        self.error_messages.append(message)

    def validate_file(self, file_reader):
        """
        Validates if required fields are present in given file
        """
        if self.required_columns:
            for field in self.required_columns:
                if field not in file_reader.fieldnames:
                    self.add_error(f"Missing column: {field}")

    # pylint: disable=inconsistent-return-statements

    def read_file(self):
        """
        Create a CSV reader and validate the file.
        """
        data_list = []
        reader = csv.DictReader(decode_utf8(self.file))

        self.validate_file(reader)

        for row in reader:
            valid_row = self.validate_row(row)
            if valid_row:
                data_list.append(row)

        return data_list

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
