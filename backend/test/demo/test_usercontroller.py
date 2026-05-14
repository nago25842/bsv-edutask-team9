# This creates fake database records for testing
from unittest.mock import Mock, patch
from src.controllers.usercontroller import UserController
MOCK_USERS = {
    "test@edutask.com": {...}
}

# @patch replaces the real database with a fake one
@patch('src.controllers.usercontroller.db')
def test_valid_email(self):
    # Tell the fake database what to return
    mock_db.users.find_one.return_value = MOCK_USERS["test@edutask.com"]
    
    # Call the real function
    result = get_user_by_email("test@edutask.com")
    
    # Check if it worked
    assert result["email"] == "test@edutask.com"