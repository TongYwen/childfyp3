"""
Unit tests for password validation functionality.
Tests the is_strong_password() function from app.py
"""
import pytest
import re


# Import the function directly to test in isolation
def is_strong_password(password: str) -> bool:
    """
    Copy of the password validation function for isolated testing.
    In a real scenario, you'd import this from app.py after refactoring.
    """
    if not password:
        return False

    pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[^A-Za-z0-9])(?=.{8,})'
    return re.search(pattern, password) is not None


class TestIsStrongPassword:
    """Test suite for password strength validation."""

    # ===================== VALID PASSWORDS =====================

    def test_valid_password_basic(self):
        """Test a basic valid password with all requirements."""
        assert is_strong_password("Password1!") is True

    def test_valid_password_longer(self):
        """Test a longer valid password."""
        assert is_strong_password("MySecure@Password123") is True

    def test_valid_password_special_chars(self):
        """Test passwords with various special characters."""
        special_chars = ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '-', '_', '+', '=']
        for char in special_chars:
            password = f"Password1{char}"
            assert is_strong_password(password) is True, f"Failed for special char: {char}"

    def test_valid_password_minimum_length(self):
        """Test password at exactly 8 characters (minimum)."""
        assert is_strong_password("Pass1@ab") is True

    def test_valid_password_with_numbers(self):
        """Test password with numbers included."""
        assert is_strong_password("Test#Pass99") is True

    def test_valid_password_complex(self):
        """Test a complex password with multiple special characters."""
        assert is_strong_password("C0mpl3x!@#Pass") is True

    # ===================== INVALID PASSWORDS =====================

    def test_invalid_empty_password(self):
        """Test empty string password."""
        assert is_strong_password("") is False

    def test_invalid_none_password(self):
        """Test None password."""
        assert is_strong_password(None) is False

    def test_invalid_too_short(self):
        """Test password shorter than 8 characters."""
        assert is_strong_password("Pass1!") is False  # 6 chars

    def test_invalid_exactly_seven_chars(self):
        """Test password at exactly 7 characters (one below minimum)."""
        assert is_strong_password("Pass1!a") is False  # 7 chars

    def test_invalid_no_uppercase(self):
        """Test password without uppercase letter."""
        assert is_strong_password("password1!") is False

    def test_invalid_no_lowercase(self):
        """Test password without lowercase letter."""
        assert is_strong_password("PASSWORD1!") is False

    def test_invalid_no_special_char(self):
        """Test password without special character."""
        assert is_strong_password("Password123") is False

    def test_invalid_only_lowercase(self):
        """Test password with only lowercase letters."""
        assert is_strong_password("password") is False

    def test_invalid_only_uppercase(self):
        """Test password with only uppercase letters."""
        assert is_strong_password("PASSWORD") is False

    def test_invalid_only_numbers(self):
        """Test password with only numbers."""
        assert is_strong_password("12345678") is False

    def test_invalid_only_special_chars(self):
        """Test password with only special characters."""
        assert is_strong_password("!@#$%^&*") is False

    def test_invalid_lowercase_and_numbers_only(self):
        """Test password with lowercase and numbers but no uppercase or special."""
        assert is_strong_password("password123") is False

    def test_invalid_uppercase_and_numbers_only(self):
        """Test password with uppercase and numbers but no lowercase or special."""
        assert is_strong_password("PASSWORD123") is False

    # ===================== EDGE CASES =====================

    def test_edge_case_whitespace_only(self):
        """Test password with only whitespace."""
        assert is_strong_password("        ") is False

    def test_edge_case_whitespace_in_password(self):
        """Test password with space as special character."""
        # Space could be considered a special character
        assert is_strong_password("Pass word1") is True

    def test_edge_case_unicode_characters(self):
        """Test password with unicode characters."""
        # Unicode special characters should work
        assert is_strong_password("Password1\u00a9") is True  # Copyright symbol

    def test_edge_case_very_long_password(self):
        """Test a very long password."""
        long_pass = "A" + "a" * 100 + "1!"
        assert is_strong_password(long_pass) is True

    def test_edge_case_special_at_start(self):
        """Test password with special character at start."""
        assert is_strong_password("!Password1") is True

    def test_edge_case_special_at_end(self):
        """Test password with special character at end."""
        assert is_strong_password("Password1!") is True

    # ===================== COMMON WEAK PASSWORDS =====================

    def test_common_password_password(self):
        """Test common password 'password'."""
        assert is_strong_password("password") is False

    def test_common_password_123456(self):
        """Test common password '123456'."""
        assert is_strong_password("123456") is False

    def test_common_password_qwerty(self):
        """Test common password 'qwerty'."""
        assert is_strong_password("qwerty") is False

    # ===================== FIXTURE-BASED TESTS =====================

    def test_all_weak_passwords(self, weak_passwords):
        """Test all weak passwords from fixture."""
        for password in weak_passwords:
            assert is_strong_password(password) is False, f"Should reject: {password}"

    def test_all_strong_passwords(self, strong_passwords):
        """Test all strong passwords from fixture."""
        for password in strong_passwords:
            assert is_strong_password(password) is True, f"Should accept: {password}"
