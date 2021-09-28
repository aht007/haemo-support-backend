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

    def add_errors_to_error_list(self, errors):
        """
        Add errors list to error_messages list
        """
        self.error_messages.extend(errors)

    def check_file_has_content(self, file_reader):
        """
        Check if file has content or not
        """
        if file_reader.fieldnames is not None:
            return True
        else:
            self.error_messages.append("File has no content")
            return False

    def validate_headers(self, file_reader):
        """
        Validates if required fields are present in given file
        """
        header_errors = []
        for field in required_columns:
            if field not in file_reader.fieldnames:
                header_errors.append(f"Missing column: {field}")
        if len(header_errors) > 0:
            self.add_errors_to_error_list(header_errors)
            return False
        return True

    def validate_file(self, file_reader):
        """
        Validate the given file for presence of content and headers
        """
        file_has_content = self.check_file_has_content(file_reader)
        if file_has_content is True:
            return self.validate_headers(file_reader)
        return False

    # pylint: disable=inconsistent-return-statements

    def parse_file(self):
        """
        Create a CSV reader Parse the File
        """
        data_list = []
        reader = csv.DictReader(decode_utf8(self.file))

        if self.validate_file(reader):
            row_parser = RowParser()
            for index, row in enumerate(reader):
                is_valid = row_parser.validate_row(index, row)
                if is_valid:
                    data_list.append(row)
                else:
                    errors_list = row_parser.row_errors
                    self.add_errors_to_error_list(errors_list)
        return data_list


class RowParser:
    """
    Parses a row data for checkings its validity
    Rows are based on User Model
    """

    def __init__(self):
        self.row_errors = []

    def validate_column(self, validator_method, index, col):
        """
        validates an individual column with the validator method passed
        returns true or add error message to the list
        """
        try:
            validator_method(col)
        except ValidationError as exc:
            self.row_errors.append(f"Row Index {index+1}: " + exc.message)

    def validate_row(self, index, row):
        """
        Return true if all columns of a row have valid data, false otherwise
        """
        self.row_errors.clear()
        self.validate_column(
            validate_username, index, row['username'])
        self.validate_column(
            validate_email, index, row['email'])
        self.validate_column(
            validate_password, index, row['password'])
        self.validate_column(
            validate_date_of_birth, index, row['date_of_birth'])
        self.validate_column(
            validate_phone_number, index, row['phone_number'])
        self.validate_column(
            validate_blood_group, index, row['blood_group'])
        if len(self.row_errors) > 0:
            return False
        return True
