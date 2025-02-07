# tests/test_validators.py
import pytest
from app.core.utils.validators import sanitize_email, sanitize_string, validate_password
from pydantic import ValidationError
from app.schemas import auth_schemas

def test_sanitize_email():
    assert sanitize_email("   Test@Example.Com  ") == "test@example.com"

def test_sanitize_string():
    assert sanitize_string("   hello world   ") == "hello world"

def test_validate_password_success():
    valid_password = "ValidPass1!"
    assert validate_password(valid_password) == valid_password

def test_validate_password_failure_length():
    with pytest.raises(ValueError, match="au moins 8 caractères"):
        validate_password("Short1!")

def test_validate_password_failure_uppercase():
    with pytest.raises(ValueError, match="une lettre majuscule"):
        validate_password("password1!")

def test_validate_password_failure_lowercase():
    with pytest.raises(ValueError, match="une lettre minuscule"):
        validate_password("PASSWORD1!")

def test_validate_password_failure_digit():
    with pytest.raises(ValueError, match="un chiffre"):
        validate_password("Password!")

def test_validate_password_failure_special():
    with pytest.raises(ValueError, match="un caractère spécial"):
        validate_password("Password1")

def test_login_request_model():
    data = {
        "email": "   USER@EXAMPLE.COM  ",
        "password": "ValidPass1!"
    }
    model = auth_schemas.LoginRequest(**data)
    assert model.email == "user@example.com"
    assert model.password == "ValidPass1!"

def test_register_request_model():
    data = {
        "email": "   NewUser@Example.COM  ",
        "password": "ComplexPass1@",
        "first_name": "  John  ",
        "last_name": "  Doe  "
    }
    model = auth_schemas.RegisterRequest(**data)
    assert model.email == "newuser@example.com"
    assert model.first_name == "John"
    assert model.last_name == "Doe"

    data_invalid = {
        "email": "user@example.com",
        "password": "simple",
        "first_name": "Alice",
        "last_name": "Smith"
    }
    with pytest.raises(ValidationError):
        auth_schemas.RegisterRequest(**data_invalid)
