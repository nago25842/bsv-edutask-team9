"""
Integration tests for DAO create method with MongoDB
PA1417 Assignment 3
"""

import pytest
import random
import string
from src.util.dao import DAO

def random_string(length=8):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

class TestDAOCreate:
    
    @pytest.fixture
    def user_dao(self):
        """Fixture for users collection - creates isolated test environment"""
        dao = DAO("user")
        yield dao
        # Clean up: delete only test documents created during tests
        dao.collection.delete_many({"email": {"$regex": "^test_"}})
        dao.collection.delete_many({"email": {"$regex": "^dup_"}})
    
    def test_create_valid_user(self, user_dao):
        """TC1: Create a valid user should succeed"""
        test_email = f"test_{random_string()}@example.com"
        user_data = {
            "email": test_email,
            "firstName": "Test",
            "lastName": "User",
            "password": "secret123"
        }
        result = user_dao.create(user_data)
        assert result is not None
        # result is a dict, not a list - access directly
        assert result["email"] == test_email
        assert result["firstName"] == "Test"
        assert result["lastName"] == "User"
    
    def test_create_missing_required_field(self, user_dao):
        """TC2: Missing required field (email) should fail"""
        invalid_data = {
            "firstName": "Test",
            "lastName": "User",
            "password": "secret123"
        }
        with pytest.raises(Exception):
            user_dao.create(invalid_data)
    
    def test_create_empty_data(self, user_dao):
        """TC3: Empty data should fail"""
        with pytest.raises(Exception):
            user_dao.create({})
    
    def test_create_invalid_data_type(self, user_dao):
        """TC4: Wrong data type for email should fail"""
        invalid_data = {
            "email": 12345,  # should be string
            "firstName": "Test",
            "lastName": "User"
        }
        with pytest.raises(Exception):
            user_dao.create(invalid_data)
    
    def test_create_duplicate_email(self, user_dao):
        """TC5: Duplicate email - check what database does"""
        test_email = f"dup_{random_string()}@example.com"
        user_data = {
            "email": test_email,
            "firstName": "First",
            "lastName": "User"
        }
        # First insert should succeed
        result1 = user_dao.create(user_data)
        assert result1 is not None
        assert result1["email"] == test_email
        
        # Second insert with same email - behavior depends on validator
        duplicate_data = {
            "email": test_email,
            "firstName": "Second",
            "lastName": "User"
        }
        # The database might allow duplicates or reject them
        # We just document what happens
        result2 = user_dao.create(duplicate_data)
        # If it succeeds, the database allows duplicates
        # If it fails, there's a unique constraint
        print(f"Duplicate insert result: {result2}")
    
    def test_create_verify_document_exists(self, user_dao):
        """TC6: After create, document should be findable"""
        test_email = f"test_{random_string()}@example.com"
        user_data = {
            "email": test_email,
            "firstName": "Test",
            "lastName": "User",
            "password": "secret123"
        }
        result = user_dao.create(user_data)
        assert result is not None
        
        # Find the document
        found = user_dao.find({"email": test_email})
        
        assert found is not None
        assert len(found) > 0
        assert found[0]["email"] == test_email