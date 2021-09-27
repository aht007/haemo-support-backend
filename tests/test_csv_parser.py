"""
Tests for csv parser service
"""
from django.core.exceptions import ValidationError
from csvparser import services

import pytest


def test_validate_username_passes():
    """
    Excpects the return value to be true for a valid username given to service
    """
    username = "Aht_123786"
    assert services.validate_username(username) is True


def test_validate_username_fails():
    """
    Given a wrong username value serivce raises and exception
    """
    username = "ab123"
    with pytest.raises(ValidationError):
        services.validate_username(username)


def test_validate_password_passes():
    """
    Excpects the return value to be true for a valid password given to service
    """
    password = "Pytestsis$pecial007"
    assert services.validate_password(password) is True


def test_validate_password_fails():
    """
    Given a wrong password value serivce raises and exception
    """
    password = "ab123"
    with pytest.raises(ValidationError):
        services.validate_password(password)


def test_validate_email_passes():
    """
    Excpects the return value to be true for a valid email given to service
    """
    email = "test@test.com"
    assert services.validate_email(email) is True


def test_validate_email_fails():
    """
    Given a wrong email value serivce raises and exception
    """
    email = "ab123@abc"
    with pytest.raises(ValidationError):
        services.validate_email(email)


def test_validate_date_of_birth_passes():
    """
    Excpects the return value to be true for a valid date_of_birth
    given to service
    """
    date_of_birth = '1999-06-03'
    assert services.validate_date_of_birth(date_of_birth) is True


def test_validate_date_of_birth_fails():
    """
    Given a wrong date_of_birth value serivce raises and exception
    """
    date_of_birth = '1999/06/03'
    with pytest.raises(ValidationError):
        services.validate_date_of_birth(date_of_birth)


def test_validate_blood_group_passes():
    """
    Excpects the return value to be true for a valid blood_group
    given to service
    """
    blood_group = "O+"
    assert services.validate_blood_group(blood_group) is True


def test_validate_blood_group_fails():
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
    with open('tests/valid_data.csv', 'r', encoding='UTF-8') as file:
        csv_parser = services.CsvParser(file)
        data = csv_parser.parse_file()
        data_dict = {}
        data_dict['data'] = data
        data_dict['errors'] = csv_parser.error_messages
        assert len(data_dict['errors']) == 0
        assert len(data_dict['data']) > 0


def test_invalid_file_data():
    """
    Tests the csv parser class functionality with invalid data
    """
    with open('tests/invalid_data.csv', 'r', encoding='UTF-8') as file:
        csv_parser = services.CsvParser(file)
        csv_parser.parse_file()
        assert len(csv_parser.error_messages) > 0
