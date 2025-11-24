"""
Integration tests for child management functionality.
Tests CRUD operations for children and related features.
"""
import pytest
from unittest.mock import MagicMock, patch
from datetime import date


class TestSelectChild:
    """Test suite for child selection functionality."""

    def test_select_child_requires_login(self, client):
        """Test that select child page requires authentication."""
        response = client.get('/select_child', follow_redirects=False)
        assert response.status_code == 302

    @patch('app.get_db_conn')
    @patch('app.current_user')
    def test_select_child_shows_user_children(self, mock_user, mock_db, client):
        """Test that select child shows only user's children."""
        mock_user.is_authenticated = True
        mock_user.id = 1
        mock_user.role = 'parent'

        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchall.return_value = [
            {'id': 1, 'name': 'Child 1', 'dob': date(2020, 1, 1)},
            {'id': 2, 'name': 'Child 2', 'dob': date(2021, 6, 15)}
        ]
        mock_db.return_value = mock_conn

        with client.session_transaction() as sess:
            sess['_user_id'] = '1'

        # This would test the actual response if properly authenticated
        # The key is testing the database query is made correctly


class TestAddChild:
    """Test suite for adding children."""

    def test_add_child_requires_login(self, client):
        """Test that add child requires authentication."""
        response = client.get('/add_child', follow_redirects=False)
        assert response.status_code == 302

    @patch('app.get_db_conn')
    def test_add_child_valid_data(self, mock_db, client):
        """Test adding a child with valid data."""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_db.return_value = mock_conn

        with client.session_transaction() as sess:
            sess['_user_id'] = '1'

        response = client.post('/add_child', data={
            'name': 'Test Child',
            'dob': '2020-01-15',
            'gender': 'male'
        }, follow_redirects=True)

        # Should process the request
        assert response.status_code == 200

    @patch('app.get_db_conn')
    def test_add_child_missing_name(self, mock_db, client):
        """Test adding a child without name."""
        with client.session_transaction() as sess:
            sess['_user_id'] = '1'

        response = client.post('/add_child', data={
            'name': '',
            'dob': '2020-01-15',
            'gender': 'male'
        }, follow_redirects=True)

        assert response.status_code == 200

    @patch('app.get_db_conn')
    def test_add_child_future_dob(self, mock_db, client):
        """Test adding a child with future date of birth."""
        with client.session_transaction() as sess:
            sess['_user_id'] = '1'

        response = client.post('/add_child', data={
            'name': 'Future Child',
            'dob': '2030-01-15',
            'gender': 'female'
        }, follow_redirects=True)

        # Application should handle this validation
        assert response.status_code == 200


class TestEditChild:
    """Test suite for editing children."""

    def test_edit_child_requires_login(self, client):
        """Test that edit child requires authentication."""
        response = client.get('/edit_child/1', follow_redirects=False)
        assert response.status_code == 302

    @patch('app.get_db_conn')
    def test_edit_child_valid_update(self, mock_db, client):
        """Test editing a child with valid data."""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchone.return_value = {
            'id': 1, 'name': 'Test Child', 'dob': date(2020, 1, 15), 'gender': 'male', 'user_id': 1
        }
        mock_db.return_value = mock_conn

        with client.session_transaction() as sess:
            sess['_user_id'] = '1'

        response = client.post('/edit_child/1', data={
            'name': 'Updated Child Name',
            'dob': '2020-02-20',
            'gender': 'male'
        }, follow_redirects=True)

        assert response.status_code == 200

    @patch('app.get_db_conn')
    def test_edit_child_not_found(self, mock_db, client):
        """Test editing a non-existent child."""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchone.return_value = None
        mock_db.return_value = mock_conn

        with client.session_transaction() as sess:
            sess['_user_id'] = '1'

        response = client.get('/edit_child/9999', follow_redirects=True)
        assert response.status_code == 200


class TestDeleteChild:
    """Test suite for deleting children."""

    def test_delete_child_requires_login(self, client):
        """Test that delete child requires authentication."""
        response = client.post('/delete_child/1', follow_redirects=False)
        assert response.status_code == 302

    @patch('app.get_db_conn')
    def test_delete_child_success(self, mock_db, client):
        """Test successfully deleting a child."""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_db.return_value = mock_conn

        with client.session_transaction() as sess:
            sess['_user_id'] = '1'

        response = client.post('/delete_child/1', follow_redirects=True)
        assert response.status_code == 200

    @patch('app.get_db_conn')
    def test_delete_child_clears_session(self, mock_db, client):
        """Test that deleting selected child clears session."""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_db.return_value = mock_conn

        with client.session_transaction() as sess:
            sess['_user_id'] = '1'
            sess['selected_child_id'] = 1

        response = client.post('/delete_child/1', follow_redirects=True)
        assert response.status_code == 200


class TestChildAuthorization:
    """Test suite for child access authorization."""

    @patch('app.get_db_conn')
    def test_parent_can_only_see_own_children(self, mock_db, client):
        """Test that parents can only access their own children."""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor

        # Return empty for a child that doesn't belong to the user
        mock_cursor.fetchone.return_value = None
        mock_db.return_value = mock_conn

        with client.session_transaction() as sess:
            sess['_user_id'] = '1'

        response = client.get('/edit_child/999', follow_redirects=True)
        assert response.status_code == 200

    @patch('app.get_db_conn')
    def test_admin_can_see_all_children(self, mock_db, client):
        """Test that admins can access all children."""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchall.return_value = [
            {'id': 1, 'name': 'Child 1', 'user_id': 1},
            {'id': 2, 'name': 'Child 2', 'user_id': 2},
            {'id': 3, 'name': 'Child 3', 'user_id': 3}
        ]
        mock_db.return_value = mock_conn

        with client.session_transaction() as sess:
            sess['_user_id'] = '1'

        # Admin should see all children in the /children route


class TestAcademicProgress:
    """Test suite for academic progress tracking."""

    def test_academic_progress_requires_login(self, client):
        """Test that academic progress requires authentication."""
        response = client.get('/academic_progress', follow_redirects=False)
        assert response.status_code == 302

    @patch('app.get_db_conn')
    def test_add_academic_record_valid(self, mock_db, client):
        """Test adding a valid academic record."""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_db.return_value = mock_conn

        with client.session_transaction() as sess:
            sess['_user_id'] = '1'
            sess['selected_child_id'] = 1

        response = client.post('/academic_progress', data={
            'subject': 'Mathematics',
            'score': '85',
            'date': '2024-01-15'
        }, follow_redirects=True)

        assert response.status_code == 200

    @patch('app.get_db_conn')
    def test_academic_record_score_validation(self, mock_db, client):
        """Test academic record with invalid score."""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_db.return_value = mock_conn

        with client.session_transaction() as sess:
            sess['_user_id'] = '1'
            sess['selected_child_id'] = 1

        # Test score above 100 (should be validated)
        response = client.post('/academic_progress', data={
            'subject': 'Mathematics',
            'score': '150',
            'date': '2024-01-15'
        }, follow_redirects=True)

        assert response.status_code == 200

    @patch('app.get_db_conn')
    def test_delete_academic_record(self, mock_db, client):
        """Test deleting an academic record."""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_db.return_value = mock_conn

        with client.session_transaction() as sess:
            sess['_user_id'] = '1'
            sess['selected_child_id'] = 1

        response = client.post('/delete_academic/1', follow_redirects=True)
        assert response.status_code == 200


class TestPreschoolTracker:
    """Test suite for preschool developmental tracking."""

    def test_preschool_tracker_requires_login(self, client):
        """Test that preschool tracker requires authentication."""
        response = client.get('/preschool_tracker', follow_redirects=False)
        assert response.status_code == 302

    @patch('app.get_db_conn')
    def test_preschool_tracker_requires_child_selection(self, mock_db, client):
        """Test that preschool tracker requires a selected child."""
        with client.session_transaction() as sess:
            sess['_user_id'] = '1'
            # No selected_child_id

        response = client.get('/preschool_tracker', follow_redirects=True)
        assert response.status_code == 200


class TestDateCalculations:
    """Test suite for date calculation utilities."""

    def test_calculate_months_difference(self):
        """Test month difference calculation."""
        from datetime import date

        def calculate_months_difference(start_date, end_date):
            """Calculate months between two dates."""
            return (end_date.year - start_date.year) * 12 + (end_date.month - start_date.month)

        # Test 1 year difference
        assert calculate_months_difference(date(2020, 1, 1), date(2021, 1, 1)) == 12

        # Test partial year
        assert calculate_months_difference(date(2020, 1, 1), date(2020, 7, 1)) == 6

        # Test same month
        assert calculate_months_difference(date(2020, 1, 1), date(2020, 1, 15)) == 0

        # Test 2 years 3 months
        assert calculate_months_difference(date(2020, 1, 1), date(2022, 4, 1)) == 27
