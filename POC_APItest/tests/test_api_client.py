# my_api_project/tests/test_api_client.py

import unittest
from api_client import APIClient
from token_generator import generate_token
from request_bodies import generate_account_body, generate_dataset_body

class TestAPIClient(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Set up environment and generate tokens
        cls.environment = "qa02"
        generate_token(cls.environment)
        cls.client = APIClient(cls.environment)

    def test_create_account(self):
        """Test the creation of an account."""
        account_data = generate_account_body("ID123", "sage50uk", "user@example.com", "auth0|123456")
        response = self.client.create_account(account_data)
        self.assertIsInstance(response, dict)
        self.assertIn("data", response)
        self.account_id = response["data"]["id"]

    def test_create_dataset(self):
        """Test the creation of a dataset."""
        self.test_create_account()  # Ensure account is created first
        dataset_data = generate_dataset_body("DatasetName", "ID123", "sage50uk")
        response = self.client.create_dataset(self.account_id, dataset_data)
        self.assertIsInstance(response, dict)
        self.assertIn("data", response)
        self.dataset_id = response["data"]["id"]

    def test_get_datasets(self):
        """Test fetching all datasets."""
        response = self.client.get_datasets()
        self.assertIsInstance(response, dict)
        self.assertIn("data", response)

    def test_get_dataset(self):
        """Test fetching a specific dataset."""
        self.test_create_dataset()  # Ensure dataset is created first
        response = self.client.get_dataset(self.dataset_id)
        self.assertIsInstance(response, dict)
        self.assertIn("data", response)
        self.assertEqual(response["data"]["id"], self.dataset_id)

    def test_get_application_client(self):
        """Test fetching application client details."""
        client_id = "client123"
        response = self.client.get_application_client(client_id)
        self.assertIsInstance(response, dict)
        self.assertIn("data", response)

    def test_get_dataset_servicefabric(self):
        """Test fetching dataset service fabric details."""
        self.test_create_dataset()  # Ensure dataset is created first
        response = self.client.get_dataset_servicefabric(self.dataset_id)
        self.assertIsInstance(response, dict)
        self.assertIn("data", response)

    def test_get_users_dataset(self):
        """Test fetching users associated with a dataset."""
        self.test_create_dataset()  # Ensure dataset is created first
        response = self.client.get_users_dataset(self.dataset_id)
        self.assertIsInstance(response, dict)
        self.assertIn("data", response)

    def test_get_users(self):
        """Test fetching user details by user ID."""
        user_id = "user123"
        response = self.client.get_users(user_id)
        self.assertIsInstance(response, dict)
        self.assertIn("data", response)

    def test_get_ledger_tenant(self):
        """Test fetching ledger tenant details."""
        self.test_create_dataset()  # Ensure dataset is created first
        response = self.client.get_ledger_tenant(self.dataset_id)
        self.assertIsInstance(response, dict)
        self.assertIn("data", response)

    def test_get_query_users_dataset(self):
        """Test querying users for a dataset."""
        self.test_create_dataset()  # Ensure dataset is created first
        response = self.client.get_query_users_dataset(self.dataset_id)
        self.assertIsInstance(response, dict)
        self.assertIn("data", response)

if __name__ == "__main__":
    unittest.main()


