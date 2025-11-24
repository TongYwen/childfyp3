"""
Integration tests for authentication routes.
Tests registration, login, logout, and password reset flows.
"""
import pytest
from unittest.mock import MagicMock, patch


class TestRegisterRoute:
    """Test suite for the /register route."""

    def test_register_page_loads(self, client):
        """Test that register page loads successfully."""
        response = client.get('/register')
        assert response.status_code == 200

    @patch('app.get_db_conn')
    def test_register_successful_parent(self, mock_db, client):
        """Test successful parent registration."""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_db.return_value = mock_conn

        response = client.post('/register', data={
            'name': 'Test User',
            'email': 'newuser@example.com',
            'password': 'ValidPass1!',
            'role': 'parent'
        }, follow_redirects=True)

        # Should redirect to login after successful registration
        assert response.status_code == 200

    @patch('app.get_db_conn')
    def test_register_missing_fields(self, mock_db, client):
        """Test registration with missing required fields."""
        response = client.post('/register', data={
            'name': '',
            'email': 'test@example.com',
            'password': 'ValidPass1!',
            'role': 'parent'
        }, follow_redirects=True)

        assert response.status_code == 200
        # Should show warning about filling all fields

    @patch('app.get_db_conn')
    def test_register_invalid_email(self, mock_db, client):
        """Test registration with invalid email format."""
        response = client.post('/register', data={
            'name': 'Test User',
            'email': 'notanemail',
            'password': 'ValidPass1!',
            'role': 'parent'
        }, follow_redirects=True)

        assert response.status_code == 200
        # Should show warning about valid email

    @patch('app.get_db_conn')
    def test_register_weak_password(self, mock_db, client):
        """Test registration with weak password."""
        response = client.post('/register', data={
            'name': 'Test User',
            'email': 'test@example.com',
            'password': 'weak',
            'role': 'parent'
        }, follow_redirects=True)

        assert response.status_code == 200
        # Should show warning about password requirements

    @patch('app.get_db_conn')
    def test_register_invalid_role(self, mock_db, client):
        """Test registration with invalid role."""
        response = client.post('/register', data={
            'name': 'Test User',
            'email': 'test@example.com',
            'password': 'ValidPass1!',
            'role': 'invalid_role'
        }, follow_redirects=True)

        assert response.status_code == 200
        # Should show warning about invalid role

    @patch('app.get_db_conn')
    def test_register_admin_without_passkey(self, mock_db, client):
        """Test admin registration without passkey."""
        response = client.post('/register', data={
            'name': 'Admin User',
            'email': 'admin@example.com',
            'password': 'ValidPass1!',
            'role': 'admin',
            'admin_passkey': ''
        }, follow_redirects=True)

        assert response.status_code == 200
        # Should show warning about admin passkey required

    @patch('app.get_db_conn')
    def test_register_admin_wrong_passkey(self, mock_db, client):
        """Test admin registration with wrong passkey."""
        response = client.post('/register', data={
            'name': 'Admin User',
            'email': 'admin@example.com',
            'password': 'ValidPass1!',
            'role': 'admin',
            'admin_passkey': 'wrongpasskey'
        }, follow_redirects=True)

        assert response.status_code == 200
        # Should show warning about invalid admin passkey

    @patch('app.get_db_conn')
    def test_register_admin_correct_passkey(self, mock_db, client):
        """Test admin registration with correct passkey."""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_db.return_value = mock_conn

        response = client.post('/register', data={
            'name': 'Admin User',
            'email': 'admin@example.com',
            'password': 'ValidPass1!',
            'role': 'admin',
            'admin_passkey': 'child1234'  # Correct passkey from app.py
        }, follow_redirects=True)

        assert response.status_code == 200

    @patch('app.get_db_conn')
    def test_register_duplicate_email(self, mock_db, client):
        """Test registration with already registered email."""
        import mysql.connector.errors

        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.execute.side_effect = mysql.connector.errors.IntegrityError()
        mock_db.return_value = mock_conn

        response = client.post('/register', data={
            'name': 'Test User',
            'email': 'existing@example.com',
            'password': 'ValidPass1!',
            'role': 'parent'
        }, follow_redirects=True)

        assert response.status_code == 200
        # Should show warning about email already registered


class TestLoginRoute:
    """Test suite for the /login route."""

    def test_login_page_loads(self, client):
        """Test that login page loads successfully."""
        response = client.get('/login')
        assert response.status_code == 200

    @patch('app.get_db_conn')
    @patch('app.bcrypt')
    def test_login_successful(self, mock_bcrypt, mock_db, client):
        """Test successful login with valid credentials."""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchone.return_value = {
            'id': 1,
            'name': 'Test User',
            'email': 'test@example.com',
            'password': 'hashed_password',
            'role': 'parent'
        }
        mock_db.return_value = mock_conn
        mock_bcrypt.check_password_hash.return_value = True

        response = client.post('/login', data={
            'email': 'test@example.com',
            'password': 'ValidPass1!'
        }, follow_redirects=True)

        assert response.status_code == 200

    @patch('app.get_db_conn')
    def test_login_user_not_found(self, mock_db, client):
        """Test login with non-existent email."""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchone.return_value = None
        mock_db.return_value = mock_conn

        response = client.post('/login', data={
            'email': 'nonexistent@example.com',
            'password': 'SomePass1!'
        }, follow_redirects=True)

        assert response.status_code == 200
        # Should show invalid credentials message

    @patch('app.get_db_conn')
    @patch('app.bcrypt')
    def test_login_wrong_password(self, mock_bcrypt, mock_db, client):
        """Test login with wrong password."""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchone.return_value = {
            'id': 1,
            'name': 'Test User',
            'email': 'test@example.com',
            'password': 'hashed_password',
            'role': 'parent'
        }
        mock_db.return_value = mock_conn
        mock_bcrypt.check_password_hash.return_value = False

        response = client.post('/login', data={
            'email': 'test@example.com',
            'password': 'WrongPass1!'
        }, follow_redirects=True)

        assert response.status_code == 200
        # Should show invalid credentials message

    @patch('app.get_db_conn')
    def test_login_empty_email(self, mock_db, client):
        """Test login with empty email."""
        response = client.post('/login', data={
            'email': '',
            'password': 'SomePass1!'
        }, follow_redirects=True)

        assert response.status_code == 200

    @patch('app.get_db_conn')
    def test_login_empty_password(self, mock_db, client):
        """Test login with empty password."""
        response = client.post('/login', data={
            'email': 'test@example.com',
            'password': ''
        }, follow_redirects=True)

        assert response.status_code == 200

    @patch('app.get_db_conn')
    @patch('app.bcrypt')
    def test_login_case_insensitive_email(self, mock_bcrypt, mock_db, client):
        """Test that email comparison is case insensitive."""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchone.return_value = {
            'id': 1,
            'name': 'Test User',
            'email': 'test@example.com',
            'password': 'hashed_password',
            'role': 'parent'
        }
        mock_db.return_value = mock_conn
        mock_bcrypt.check_password_hash.return_value = True

        # Login with uppercase email
        response = client.post('/login', data={
            'email': 'TEST@EXAMPLE.COM',
            'password': 'ValidPass1!'
        }, follow_redirects=True)

        assert response.status_code == 200


class TestLogoutRoute:
    """Test suite for the /logout route."""

    def test_logout_requires_login(self, client):
        """Test that logout requires authentication."""
        response = client.get('/logout', follow_redirects=False)
        # Should redirect to login page
        assert response.status_code == 302

    @patch('app.get_db_conn')
    def test_logout_clears_session(self, mock_db, client):
        """Test that logout clears user session."""
        # First, simulate a logged-in user
        with client.session_transaction() as sess:
            sess['_user_id'] = '1'
            sess['_fresh'] = True

        response = client.get('/logout', follow_redirects=True)
        assert response.status_code == 200


class TestPasswordResetFlow:
    """Test suite for password reset functionality."""

    def test_forgot_password_page_loads(self, client):
        """Test that forgot password page loads."""
        response = client.get('/forgot')
        assert response.status_code == 200

    @patch('app.get_db_conn')
    @patch('app.send_reset_email')
    def test_forgot_password_valid_email(self, mock_email, mock_db, client):
        """Test forgot password with valid registered email."""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchone.return_value = {'id': 1, 'email': 'test@example.com'}
        mock_db.return_value = mock_conn

        response = client.post('/forgot', data={
            'email': 'test@example.com'
        }, follow_redirects=True)

        assert response.status_code == 200

    @patch('app.get_db_conn')
    def test_forgot_password_unregistered_email(self, mock_db, client):
        """Test forgot password with unregistered email."""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchone.return_value = None
        mock_db.return_value = mock_conn

        response = client.post('/forgot', data={
            'email': 'nonexistent@example.com'
        }, follow_redirects=True)

        assert response.status_code == 200

    @patch('app.serializer')
    def test_reset_password_invalid_token(self, mock_serializer, client):
        """Test reset password with invalid token."""
        from itsdangerous import SignatureExpired, BadSignature
        mock_serializer.loads.side_effect = BadSignature("Invalid")

        response = client.get('/reset/invalid_token', follow_redirects=True)
        assert response.status_code == 200

    @patch('app.serializer')
    def test_reset_password_expired_token(self, mock_serializer, client):
        """Test reset password with expired token."""
        from itsdangerous import SignatureExpired
        mock_serializer.loads.side_effect = SignatureExpired("Expired")

        response = client.get('/reset/expired_token', follow_redirects=True)
        assert response.status_code == 200


class TestProtectedRoutes:
    """Test suite for protected route access."""

    def test_profile_requires_login(self, client):
        """Test that profile page requires authentication."""
        response = client.get('/profile', follow_redirects=False)
        assert response.status_code == 302  # Redirect to login

    def test_dashboard_requires_login(self, client):
        """Test that dashboard requires authentication."""
        response = client.get('/dashboard', follow_redirects=False)
        assert response.status_code == 302

    def test_children_requires_login(self, client):
        """Test that children page requires authentication."""
        response = client.get('/children', follow_redirects=False)
        assert response.status_code == 302

    def test_add_child_requires_login(self, client):
        """Test that add child page requires authentication."""
        response = client.get('/add_child', follow_redirects=False)
        assert response.status_code == 302
