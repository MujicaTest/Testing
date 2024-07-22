# my_api_project/tests/test_api_client.py
import unittest
from api_client import APIClient
from sageid_automation import sageid_auth, SageIDAuthAutomation
from token_generator import generate_token
from request_bodies import generate_account_body, generate_dataset_body
from sageid_auth import SageIDAuthAutomation
from POC_APItest.tests.random_utils import get_random_character, get_random_company, generate_random_uuid, get_random_sage_products
class TestAPIClient(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Set up environment and generate tokens
        cls.environment = "qa02"
        # Generate tokens using SageIDAuthAutomation
        sageid_auth = SageIDAuthAutomation(
            client_id="2VTkNzE3St3yShVbZ2cnlkhQVBUHxves",
            redirect_uri="https://id-shadow.sage.com/mobile",
            scope="openid email profile offline_access user:full",
            audience="SBCDS/global",
            username="test.user4@sage.mailinator.com",
            password="sageworks",
            verbose=False
        )
        cls.access_token = sageid_auth.get_access_token()
        generate_token(cls.environment)
        cls.client = APIClient(cls.environment)
        # Generate and store random values
        cls.random_uuid = generate_random_uuid()
        cls.random_sage_product = get_random_sage_products()
        cls.random_company = get_random_company()

    def test_create_account(self):
        """Test the creation of an account."""
        account_data = generate_account_body(self.random_uuid,self.random_sage_product, "user@example.com", "auth0|123456")
        response = self.client.create_account(account_data)
        self.assertIsInstance(response, dict)
        self.assertIn("data", response)
        self.account_id = response["data"]["id"]

    def test_create_dataset(self):
        """Test the creation of a dataset."""
        self.test_create_account()  # Ensure account is created first
        dataset_data = generate_dataset_body(get_random_company(), self.random_uuid, self.random_sage_product)
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


