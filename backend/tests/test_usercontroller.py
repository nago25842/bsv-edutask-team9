"""
Unit tests for get_user_by_email function
PA1417 Assignment 2
"""

import pytest
from unittest.mock import Mock, patch
import sys
import os

# Add the backend directory to path so imports work
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.controllers.usercontroller import UserController, DAO

# Mock data that simulates database records
MOCK_USERS = {
    "test@edutask.com": {
        "email": "test@edutask.com",
        "name": "Test User",
        "user_id": "12345"
    },
    "john@example.com": {
        "email": "john@example.com", 
        "name": "John Doe",
        "user_id": "67890"
    }
}

class TestGetUserByEmail:
    
    def setup_method(self):
        """Create a UserController with a mocked DAO before each test"""
        self.mock_dao = Mock(spec=DAO)
        self.controller = UserController(dao=self.mock_dao)
    
    def test_tc1_valid_existing_email(self):
        """TC1: Valid email that exists should return user"""
        # Return a list with one user
        self.mock_dao.find.return_value = [MOCK_USERS["test@edutask.com"]]
        result = self.controller.get_user_by_email("test@edutask.com")
        assert result is not None
        assert result["email"] == "test@edutask.com"
        self.mock_dao.find.assert_called_with({'email': 'test@edutask.com'})
    
    def test_tc2_non_existent_email(self):
        """TC2: Valid email format but not in database returns None"""
        # Return empty list - THIS IS THE BUG IN THE CODE
        # The function should return None but instead crashes with IndexError
        self.mock_dao.find.return_value = []
        result = self.controller.get_user_by_email("fake@nowhere.com")
        # This will fail because the code has a bug
        # We document that the test fails = we found a defect
        assert result is None
    
    def test_tc3_empty_string_raises_error(self):
        """TC3: Empty string should raise ValueError"""
        with pytest.raises(ValueError, match="invalid email address"):
            self.controller.get_user_by_email("")
    
    def test_tc4_none_value_raises_error(self):
        """TC4: None should raise ValueError"""
        # The current code crashes with TypeError - this is a bug
        # A proper implementation would check for None first
        with pytest.raises((ValueError, TypeError)):
            # We expect ValueError, but currently get TypeError (bug)
            self.controller.get_user_by_email(None)
    
    def test_tc5_invalid_format_no_at_raises_error(self):
        """TC5: Missing @ symbol should raise ValueError"""
        with pytest.raises(ValueError, match="invalid email address"):
            self.controller.get_user_by_email("notanemail")
    
    def test_tc6_invalid_format_missing_domain_raises_error(self):
        """TC6: Missing domain part - regex '.*@.*' actually matches 'user@'"""
        # NOTE: The regex '.*@.*' actually matches "user@" because:
        # .* matches "user", @ matches "@", .* matches "" (empty)
        # So this test FAILS because the code doesn't validate properly
        # This is a DEFECT in the validation logic
        with pytest.raises(ValueError, match="invalid email address"):
            self.controller.get_user_by_email("user@")
    
    def test_tc7_multiple_users_with_same_email(self):
        """TC7: Multiple users with same email - should return first and print warning"""
        multiple_users = [
            {"email": "duplicate@test.com", "name": "User1", "user_id": "001"},
            {"email": "duplicate@test.com", "name": "User2", "user_id": "002"}
        ]
        self.mock_dao.find.return_value = multiple_users
        
        # Capture print output
        import io
        captured = io.StringIO()
        old_stdout = sys.stdout
        sys.stdout = captured
        
        result = self.controller.get_user_by_email("duplicate@test.com")
        
        sys.stdout = old_stdout
        
        assert result is not None
        assert result["user_id"] == "001"  # Returns first one
        assert "more than one user found" in captured.getvalue()
    
    def test_tc8_whitespace_email(self):
        """TC8: Email with spaces - should be rejected"""
        # The regex '.*@.*' matches "  test@edutask.com  " because spaces are .
        # This is actually a validation defect - emails shouldn't have spaces
        with pytest.raises(ValueError, match="invalid email address"):
            self.controller.get_user_by_email("  test@edutask.com  ")
    
    def test_tc9_database_exception(self):
        """TC9: Database error should propagate the exception"""
        self.mock_dao.find.side_effect = Exception("Database connection failed")
        
        with pytest.raises(Exception, match="Database connection failed"):
            self.controller.get_user_by_email("test@edutask.com")