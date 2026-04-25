"""
Integration tests for DAO create method with MongoDB
PA1417 Assignment 3
"""

import pytest
from src.util.dao import DAO
import random
import string

def random_string(length=8):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

class TestDAOCreate:
    
    @pytest.fixture
    def user_dao(self):
        """Fixture for users collection"""
        dao = DAO("user")
        yield dao
        # Clean up after test
        dao.collection.delete_many({"email": {"$regex": "^test_"}})
    
    def test_create_valid_user(self, user_dao):
        """TC1: Create a valid user should succeed"""
        test_email = f"test_{random_string()}@example.com"
        user_data = {
            "email": test_email,
            "password": "secret123",
            "name": "Test User"
        }
        
        result = user_dao.create(user_data)
        
        assert result is not None
        assert result[0]["email"] == test_email
    
    def test_create_missing_required_field(self, user_dao):
        """TC2: Missing required field (email) should fail"""
        invalid_data = {
            "password": "secret123",
            "name": "No Email User"
        }
        
        with pytest.raises(Exception):
            user_dao.create(invalid_data)
    
    def test_create_empty_data(self, user_dao):
        """TC3: Empty data should fail"""
        with pytest.raises(Exception):
            user_dao.create({})
    
    def test_create_invalid_data_type(self, user_dao):
        """TC4: Wrong data type should fail"""
        test_email = f"test_{random_string()}@example.com"
        invalid_data = {
            "email": 12345,  # should be string
            "password": "secret123",
            "name": "Test User"
        }
        
        with pytest.raises(Exception):
            user_dao.create(invalid_data)
    
    def test_create_duplicate_email(self, user_dao):
        """TC5: Duplicate email should fail"""
        test_email = f"dup_{random_string()}@example.com"
        user_data = {
            "email": test_email,
            "password": "secret123",
            "name": "First User"
        }
        
        # First insert should work
        user_dao.create(user_data)
        
        # Second insert with same email should fail
        duplicate_data = {
            "email": test_email,
            "password": "secret123",
            "name": "Second User"
        }
        
        with pytest.raises(Exception):
            user_dao.create(duplicate_data)
    
    def test_create_verify_document_exists(self, user_dao):
        """TC6: After create, document should be findable"""
        test_email = f"test_{random_string()}@example.com"
        user_data = {
            "email": test_email,
            "password": "secret123",
            "name": "Test User"
        }
        
        result = user_dao.create(user_data)
        
        # Try to find it
        found = user_dao.find({"email": test_email})
        
        assert found is not None
        assert len(found) > 0
        assert found[0]["email"] == test_email