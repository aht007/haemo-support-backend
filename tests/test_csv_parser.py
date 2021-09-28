"""
Tests for csv parser service
"""
from django.core.exceptions import ValidationError
from csvparser import services

import pytest


def read_csv_file(file_path):
    """
    Parse a csv file using the path given as argument
    and returns parsed data dictionary
    """
    with open(file_path, 'r', encoding='UTF-8') as file:
        csv_parser = services.CsvParser(file)
        data = csv_parser.parse_file()
        data_dict = {}
        data_dict['data'] = data
        data_dict['errors'] = csv_parser.error_messages
        return data_dict


def test_valid_username():
    """
    Excpects the return value to be true for a valid username given to service
    """
    username = "Aht_123786"
    assert services.validate_username(username) is True


def test_invalid_username():
    """
    Given a wrong username value serivce raises and exception
    """
    username = "ab123"
    with pytest.raises(ValidationError):
        services.validate_username(username)


def test_valid_password():
    """
    Excpects the return value to be true for a valid password given to service
    """
    password = "Pytestsis$pecial007"
    assert services.validate_password(password) is True


def test_invalid_password():
    """
    Given a wrong password value serivce raises and exception
    """
    password = "ab123"
    with pytest.raises(ValidationError):
        services.validate_password(password)


def test_valid_email():
    """
    Excpects the return value to be true for a valid email given to service
    """
    email = "test@test.com"
    assert services.validate_email(email) is True


def test_invalid_email():
    """
    Given a wrong email value serivce raises and exception
    """
    email = "ab123@abc"
    with pytest.raises(ValidationError):
        services.validate_email(email)


def test_valid_date_of_birth():
    """
    Excpects the return value to be true for a valid date_of_birth
    given to service
    """
    date_of_birth = '1999-06-03'
    assert services.validate_date_of_birth(date_of_birth) is True


def test_invalid_date_of_birth():
    """
    Given a wrong date_of_birth value serivce raises and exception
    """
    date_of_birth = '1999/06/03'
    with pytest.raises(ValidationError):
        services.validate_date_of_birth(date_of_birth)


def test_valid_blood_group():
    """
    Excpects the return value to be true for a valid blood_group
    given to service
    """
    blood_group = "O+"
    assert services.validate_blood_group(blood_group) is True


def test_invalid_blood_group():
    """
    Given a wrong blood_group value serivce raises and exception
    """
    blood_group = "ABC+"
    with pytest.raises(ValidationError):
        services.validate_blood_group(blood_group)


def test_valid_file_data():
    """
    Tests the csv parser class functionality with valid data
    """
    data_dict = read_csv_file('tests/valid_data.csv')
    assert len(data_dict['errors']) == 0
    assert len(data_dict['data']) > 0


def test_invalid_file_data():
    """
    Tests the csv parser class functionality with invalid data
    """
    data_dict = read_csv_file('tests/invalid_data.csv')
    assert len(data_dict['errors']) > 0


def test_empty_file_content():
    """
    Tests the csv parser class functionality with missing file
    Headers expects to return error list having missing header names
    """
    data_dict = read_csv_file('tests/empty.csv')
    assert len(data_dict['errors']) > 0


def test_missing_csv_file_headers():
    """
    Tests the csv parser class functionality with empty file
    Expects to return error list having message for empty file
    """
    data_dict = read_csv_file('tests/missing_headers.csv')
    assert len(data_dict['errors']) > 0
