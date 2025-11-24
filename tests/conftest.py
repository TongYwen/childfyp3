"""
Shared pytest fixtures for ChildGrowth Insights tests.
"""
import pytest
import sys
import os
from unittest.mock import MagicMock, patch

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


@pytest.fixture
def mock_db_connection():
    """Mock database connection for unit tests."""
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    return mock_conn, mock_cursor


@pytest.fixture
def mock_genai():
    """Mock Google Generative AI for tests."""
    with patch('google.generativeai.configure') as mock_configure:
        with patch('google.generativeai.GenerativeModel') as mock_model:
            mock_response = MagicMock()
            mock_response.text = "Mock AI response"
            mock_model.return_value.generate_content.return_value = mock_response
            yield mock_model


@pytest.fixture
def app():
    """Create and configure a test Flask application instance."""
    # Mock external dependencies before importing app
    with patch('mysql.connector.connect') as mock_connect:
        with patch('google.generativeai.configure'):
            with patch('pandas.read_csv') as mock_csv:
                # Create mock DataFrame for benchmark data
                import pandas as pd
                mock_csv.return_value = pd.DataFrame({
                    'Category': ['Motor', 'Language'],
                    'Milestone': ['Walking', 'Speaking'],
                    'Age': ['12 months', '18 months']
                })

                # Mock DB connection
                mock_conn = MagicMock()
                mock_cursor = MagicMock()
                mock_conn.cursor.return_value = mock_cursor
                mock_connect.return_value = mock_conn

                from app import app as flask_app

                flask_app.config.update({
                    'TESTING': True,
                    'WTF_CSRF_ENABLED': False,
                    'SECRET_KEY': 'test-secret-key',
                    'SERVER_NAME': 'localhost',
                })

                yield flask_app


@pytest.fixture
def client(app):
    """Create a test client for the Flask application."""
    return app.test_client()


@pytest.fixture
def app_context(app):
    """Create an application context for tests."""
    with app.app_context():
        yield


@pytest.fixture
def sample_user():
    """Sample user data for testing."""
    return {
        'id': 1,
        'name': 'Test User',
        'email': 'test@example.com',
        'password': 'TestPass123!',
        'role': 'parent'
    }


@pytest.fixture
def sample_admin():
    """Sample admin user data for testing."""
    return {
        'id': 2,
        'name': 'Admin User',
        'email': 'admin@example.com',
        'password': 'AdminPass123!',
        'role': 'admin'
    }


@pytest.fixture
def sample_child():
    """Sample child data for testing."""
    return {
        'id': 1,
        'name': 'Test Child',
        'dob': '2020-01-15',
        'gender': 'male',
        'user_id': 1
    }


@pytest.fixture
def sample_academic_record():
    """Sample academic record for testing."""
    return {
        'id': 1,
        'child_id': 1,
        'subject': 'Mathematics',
        'score': 85,
        'date': '2024-01-15'
    }


@pytest.fixture
def authenticated_client(client, app, sample_user):
    """Create an authenticated test client."""
    with client.session_transaction() as sess:
        sess['_user_id'] = str(sample_user['id'])
        sess['_fresh'] = True
    return client


@pytest.fixture
def weak_passwords():
    """Collection of weak passwords for testing."""
    return [
        '',                    # Empty
        'short',               # Too short
        'alllowercase1!',      # No uppercase
        'ALLUPPERCASE1!',      # No lowercase
        'NoSpecialChar1',      # No special character
        'Pass1!',              # Too short (6 chars)
        'password',            # Common password, no requirements
        '12345678',            # Numbers only
    ]


@pytest.fixture
def strong_passwords():
    """Collection of strong passwords for testing."""
    return [
        'Password1!',
        'MySecure@Pass123',
        'Test#Password99',
        'Str0ng!Pass',
        'Complex$Pass1',
        'Valid_Pass123!',
    ]


@pytest.fixture
def invalid_emails():
    """Collection of invalid email addresses for testing."""
    return [
        '',
        'notanemail',
        '@nodomain.com',
        'no@domain',
        'spaces in@email.com',
        'missing@.com',
        '@.com',
    ]


@pytest.fixture
def valid_emails():
    """Collection of valid email addresses for testing."""
    return [
        'test@example.com',
        'user.name@domain.org',
        'email+tag@gmail.com',
        'valid123@sub.domain.com',
    ]
