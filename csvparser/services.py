# pylint: disable=no-else-raise
"""
CSV Parser Service
"""
import csv
import re

from django.core.exceptions import ValidationError

required_columns = ['username', 'email', 'password',
                    'date_of_birth', 'phone_number', 'blood_group']
blood_group_types = ['A+', 'B+', 'O+', 'AB+', 'AB-', 'O-', 'B-', 'A-']


def decode_utf8(input_iterator):
    """
    Generator that decodes a utf-8 encoded
    file input line by line
    """
    for line in input_iterator:
        yield line if isinstance(line, str) else line.decode('utf-8')


def validate_username(value):
    """
    Validates username column using regex
    """
    reg = re.compile(
        r'[A-Za-z][A-Za-z0-9_]{7,29}')
    if not reg.match(value):
        raise ValidationError(f'{value} is not valid for column username')
    else:
        return True


def validate_email(value):
    """
    Validates email column using regex
    """
    reg = re.compile(
        r'(?=.{1,64}@)[A-Za-z0-9_-]+(\\.[A-Za-z0-9_-]+)*@[^-][A-Za-z0-9-]+(\\.'
        '[A-Za-z0-9-]+)*(\\.[A-Za-z]{2,})')
    if not reg.match(value):
        raise ValidationError(f'{value} is not valid for column email')
    else:
        return True


def validate_password(value):
    """
    Validates password column using regex
    """
    reg = re.compile(r'(?=.*[a-z])(?=.*[A-Z])[A-Za-z\d@$!#%*?&]{8,18}')
    if not reg.match(value):
        raise ValidationError(f'{value} is not valid for column password')
    else:
        return True


def validate_date_of_birth(value):
    """
    Validates Date of birth column using regex
    """
    reg = re.compile(
        '((?:19|20)[0-9][0-9])-(0?[1-9]|1[012])-(0?[1-9]|[12][0-9]|3[01])')
    if not reg.match(value):
        raise ValidationError(f'{value} is not valid for column date_of_birth')
    else:
        return True


def validate_phone_number(value):
    """
    Validates phone number column using regex
    """
    reg = re.compile(r'\+?1?\d{9,15}')
    if not reg.match(value):
        raise ValidationError(f'{value} is not valid for column phone_number')
    else:
        return True


def validate_blood_group(value):
    """
    Validates Blood grouo column
    """
    if value in blood_group_types:
        return True
    else:
        raise ValidationError(f'{value} is not valid for column blood_group')


class CsvParser:
    """
    CSV Parser Class for adding bulk donor users
    """

    def __init__(self, file):
        self.file = file
        self.error_messages = []

    def add_error(self, message):
        """
        Add an error message to error_messages list
        """
        self.error_messages.append(message)

    def validate_headers(self, file_reader):
        """
        Validates if required fields are present in given file
        """
        for field in required_columns:
            if field not in file_reader.fieldnames:
                self.add_error(f"Missing column: {field}")
                return False
        return True

    # pylint: disable=inconsistent-return-statements

    def parse_file(self):
        """
        Create a CSV reader Parse the File
        """
        data_list = []
        reader = csv.DictReader(decode_utf8(self.file))

        if self.validate_headers(reader):
            for index, row in enumerate(reader):
                valid_row = self.validate_row(index, row)
                if valid_row:
                    data_list.append(row)
            return data_list
        else:
            return data_list

    def validate_row(self, index, row):
        """
        Validate the fields in the row.
        if valid return true else add error to error variable and return false
        """
        return self.validate_columns(index, row)

    def validate_columns(self, index, row):
        """
        Return true if all columns of a row have valid data, false otherwise
        """
        old_errors_count = len(self.error_messages)
        self.validate_column_or_add_error(
            validate_username, index, row['username'])
        self.validate_column_or_add_error(
            validate_email, index, row['email'])
        self.validate_column_or_add_error(
            validate_password, index, row['password'])
        self.validate_column_or_add_error(
            validate_date_of_birth, index, row['date_of_birth'])
        self.validate_column_or_add_error(
            validate_phone_number, index, row['phone_number'])
        self.validate_column_or_add_error(
            validate_blood_group, index, row['blood_group'])
        current_error_count = len(self.error_messages)
        if current_error_count != old_errors_count:
            return False
        else:
            return True

    def validate_column_or_add_error(self, validator_method, index, col):
        """
        validates an individual column with the validator method passed
        returns true or add error message to the list
        """
        try:
            validator_method(col)
        except ValidationError as exc:
            self.add_error(f"Column Index {index}: " + exc.message)
