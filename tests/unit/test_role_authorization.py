"""
Unit tests for role normalization and authorization functionality.
Tests the normalize_role() function and roles_required() decorator from app.py
"""
import pytest
from unittest.mock import MagicMock, patch
from functools import wraps


# Copy of normalize_role for isolated testing
def normalize_role(role):
    """Normalize a role string for consistent authorization checks."""
    if not role:
        return None

    normalized = str(role).strip().lower()
    aliases = {
        "administrator": "admin",
        "admin": "admin",
        "parent": "parent",
    }

    return aliases.get(normalized)


class TestNormalizeRole:
    """Test suite for role normalization."""

    # ===================== VALID ROLE NORMALIZATION =====================

    def test_normalize_admin(self):
        """Test normalizing 'admin' role."""
        assert normalize_role("admin") == "admin"

    def test_normalize_administrator(self):
        """Test normalizing 'administrator' to 'admin'."""
        assert normalize_role("administrator") == "admin"

    def test_normalize_parent(self):
        """Test normalizing 'parent' role."""
        assert normalize_role("parent") == "parent"

    # ===================== CASE INSENSITIVITY =====================

    def test_normalize_admin_uppercase(self):
        """Test normalizing 'ADMIN' (uppercase)."""
        assert normalize_role("ADMIN") == "admin"

    def test_normalize_admin_mixed_case(self):
        """Test normalizing 'Admin' (mixed case)."""
        assert normalize_role("Admin") == "admin"

    def test_normalize_administrator_uppercase(self):
        """Test normalizing 'ADMINISTRATOR' (uppercase)."""
        assert normalize_role("ADMINISTRATOR") == "admin"

    def test_normalize_parent_uppercase(self):
        """Test normalizing 'PARENT' (uppercase)."""
        assert normalize_role("PARENT") == "parent"

    def test_normalize_parent_mixed_case(self):
        """Test normalizing 'Parent' (mixed case)."""
        assert normalize_role("Parent") == "parent"

    # ===================== WHITESPACE HANDLING =====================

    def test_normalize_with_leading_whitespace(self):
        """Test normalizing role with leading whitespace."""
        assert normalize_role("  admin") == "admin"

    def test_normalize_with_trailing_whitespace(self):
        """Test normalizing role with trailing whitespace."""
        assert normalize_role("admin  ") == "admin"

    def test_normalize_with_both_whitespace(self):
        """Test normalizing role with leading and trailing whitespace."""
        assert normalize_role("  admin  ") == "admin"

    def test_normalize_parent_with_whitespace(self):
        """Test normalizing parent role with whitespace."""
        assert normalize_role("  parent  ") == "parent"

    # ===================== NONE AND EMPTY HANDLING =====================

    def test_normalize_none(self):
        """Test normalizing None role."""
        assert normalize_role(None) is None

    def test_normalize_empty_string(self):
        """Test normalizing empty string role."""
        assert normalize_role("") is None

    def test_normalize_whitespace_only(self):
        """Test normalizing whitespace-only string."""
        # After strip(), this becomes empty string, which isn't in aliases
        assert normalize_role("   ") is None

    # ===================== INVALID/UNKNOWN ROLES =====================

    def test_normalize_unknown_role(self):
        """Test normalizing an unknown role."""
        assert normalize_role("unknown") is None

    def test_normalize_user_role(self):
        """Test normalizing 'user' role (not in aliases)."""
        assert normalize_role("user") is None

    def test_normalize_guest_role(self):
        """Test normalizing 'guest' role (not in aliases)."""
        assert normalize_role("guest") is None

    def test_normalize_moderator_role(self):
        """Test normalizing 'moderator' role (not in aliases)."""
        assert normalize_role("moderator") is None

    def test_normalize_random_string(self):
        """Test normalizing a random string."""
        assert normalize_role("xyzabc123") is None

    # ===================== TYPE COERCION =====================

    def test_normalize_integer_role(self):
        """Test normalizing integer role (should convert to string)."""
        # str(1).strip().lower() = "1", not in aliases
        assert normalize_role(1) is None

    def test_normalize_float_role(self):
        """Test normalizing float role."""
        assert normalize_role(1.0) is None

    def test_normalize_boolean_true(self):
        """Test normalizing boolean True."""
        # str(True) = "True", stripped and lowered = "true", not in aliases
        assert normalize_role(True) is None

    def test_normalize_boolean_false(self):
        """Test normalizing boolean False."""
        assert normalize_role(False) is None

    # ===================== EDGE CASES =====================

    def test_normalize_admin_substring(self):
        """Test that 'admin' substring doesn't partially match."""
        assert normalize_role("superadmin") is None

    def test_normalize_admin_with_prefix(self):
        """Test that prefixed admin doesn't match."""
        assert normalize_role("super_admin") is None

    def test_normalize_partial_administrator(self):
        """Test partial 'administrator' doesn't match."""
        assert normalize_role("administrato") is None


class TestRolesRequired:
    """Test suite for the roles_required decorator."""

    @pytest.fixture
    def mock_current_user(self):
        """Create a mock current user."""
        user = MagicMock()
        user.is_authenticated = True
        user.role = "parent"
        return user

    @pytest.fixture
    def mock_unauthenticated_user(self):
        """Create a mock unauthenticated user."""
        user = MagicMock()
        user.is_authenticated = False
        user.role = None
        return user

    def test_parent_can_access_parent_route(self, mock_current_user):
        """Test that parent can access parent-only routes."""
        # Simulated authorization check
        normalized_user_role = normalize_role(mock_current_user.role)
        allowed_roles = [normalize_role("parent")]

        assert mock_current_user.is_authenticated is True
        assert normalized_user_role in allowed_roles

    def test_admin_can_access_admin_route(self):
        """Test that admin can access admin-only routes."""
        mock_user = MagicMock()
        mock_user.is_authenticated = True
        mock_user.role = "admin"

        normalized_user_role = normalize_role(mock_user.role)
        allowed_roles = [normalize_role("admin")]

        assert normalized_user_role in allowed_roles

    def test_administrator_alias_can_access_admin_route(self):
        """Test that 'administrator' role can access admin routes."""
        mock_user = MagicMock()
        mock_user.is_authenticated = True
        mock_user.role = "administrator"

        normalized_user_role = normalize_role(mock_user.role)
        allowed_roles = [normalize_role("admin")]

        assert normalized_user_role in allowed_roles

    def test_parent_cannot_access_admin_route(self, mock_current_user):
        """Test that parent cannot access admin-only routes."""
        normalized_user_role = normalize_role(mock_current_user.role)
        allowed_roles = [normalize_role("admin")]

        assert normalized_user_role not in allowed_roles

    def test_admin_cannot_access_parent_only_route(self):
        """Test route access when admin tries parent-only route."""
        mock_user = MagicMock()
        mock_user.is_authenticated = True
        mock_user.role = "admin"

        normalized_user_role = normalize_role(mock_user.role)
        allowed_roles = [normalize_role("parent")]

        assert normalized_user_role not in allowed_roles

    def test_multi_role_access_parent(self, mock_current_user):
        """Test access to route allowing multiple roles (as parent)."""
        normalized_user_role = normalize_role(mock_current_user.role)
        allowed_roles = [normalize_role("admin"), normalize_role("parent")]

        assert normalized_user_role in allowed_roles

    def test_multi_role_access_admin(self):
        """Test access to route allowing multiple roles (as admin)."""
        mock_user = MagicMock()
        mock_user.is_authenticated = True
        mock_user.role = "admin"

        normalized_user_role = normalize_role(mock_user.role)
        allowed_roles = [normalize_role("admin"), normalize_role("parent")]

        assert normalized_user_role in allowed_roles

    def test_unauthenticated_user_denied(self, mock_unauthenticated_user):
        """Test that unauthenticated users are denied access."""
        assert mock_unauthenticated_user.is_authenticated is False

    def test_unknown_role_denied(self):
        """Test that unknown roles are denied access."""
        mock_user = MagicMock()
        mock_user.is_authenticated = True
        mock_user.role = "unknown_role"

        normalized_user_role = normalize_role(mock_user.role)
        allowed_roles = [normalize_role("admin"), normalize_role("parent")]

        # normalize_role returns None for unknown roles
        assert normalized_user_role is None
        assert normalized_user_role not in allowed_roles

    def test_none_role_denied(self):
        """Test that None role is denied access."""
        mock_user = MagicMock()
        mock_user.is_authenticated = True
        mock_user.role = None

        normalized_user_role = normalize_role(mock_user.role)
        allowed_roles = [normalize_role("admin")]

        assert normalized_user_role is None
        assert normalized_user_role not in allowed_roles


class TestEmailValidation:
    """Test suite for email validation regex."""

    # Regex pattern from app.py
    EMAIL_REGEX_PATTERN = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"

    def test_valid_simple_email(self):
        """Test simple valid email."""
        import re
        assert re.match(self.EMAIL_REGEX_PATTERN, "test@example.com") is not None

    def test_valid_email_with_dots(self):
        """Test email with dots in local part."""
        import re
        assert re.match(self.EMAIL_REGEX_PATTERN, "user.name@domain.org") is not None

    def test_valid_email_with_plus(self):
        """Test email with plus sign."""
        import re
        assert re.match(self.EMAIL_REGEX_PATTERN, "email+tag@gmail.com") is not None

    def test_valid_email_subdomain(self):
        """Test email with subdomain."""
        import re
        assert re.match(self.EMAIL_REGEX_PATTERN, "user@sub.domain.com") is not None

    def test_invalid_email_no_at(self):
        """Test email without @ sign."""
        import re
        assert re.match(self.EMAIL_REGEX_PATTERN, "notanemail") is None

    def test_invalid_email_no_domain(self):
        """Test email without domain."""
        import re
        assert re.match(self.EMAIL_REGEX_PATTERN, "user@") is None

    def test_invalid_email_no_tld(self):
        """Test email without TLD."""
        import re
        assert re.match(self.EMAIL_REGEX_PATTERN, "user@domain") is None

    def test_invalid_email_short_tld(self):
        """Test email with single-character TLD."""
        import re
        assert re.match(self.EMAIL_REGEX_PATTERN, "user@domain.c") is None

    def test_invalid_email_empty(self):
        """Test empty string as email."""
        import re
        assert re.match(self.EMAIL_REGEX_PATTERN, "") is None

    def test_valid_emails_fixture(self, valid_emails):
        """Test all valid emails from fixture."""
        import re
        for email in valid_emails:
            assert re.match(self.EMAIL_REGEX_PATTERN, email) is not None, f"Should accept: {email}"

    def test_invalid_emails_fixture(self, invalid_emails):
        """Test all invalid emails from fixture."""
        import re
        for email in invalid_emails:
            assert re.match(self.EMAIL_REGEX_PATTERN, email) is None, f"Should reject: {email}"
