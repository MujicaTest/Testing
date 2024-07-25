# POC_APItest/api_client.py
import requests
import json
import uuid
import time
from config import Config, ENDPOINTS
from sageid_auth import SageIDAuthAutomation
import configparser

class APIClient:
    def __init__(self, environment, token_file="m2m_token.json", user_token_file="user_token.json"):
        # Set base URL based on environment
        self.base_url = Config.get_base_url(environment)
        if not self.base_url:
            raise ValueError(f"Invalid environment: {environment}")
        # Read tokens from files
        self.token = self._read_token(token_file)
        self.user_token = self._read_token(user_token_file)
        
    def __init__(self, client_id, redirect_uri, scope, audience, username, password, verbose=False):
        self.auth = SageIDAuthAutomation(client_id, redirect_uri, scope, audience, username, password, verbose)
        self.base_url = "https://api.example.com"
        self.token = self.get_bearer_token()

    def get_bearer_token(self):
        # Generate and save the token
        self.auth.get_access_token()
        
        # Read the token from the file
        with open("user_token.json", "r") as file:
            token_data = json.load(file)
        return token_data["token"]

    def _read_token(self, token_file):
        """Read token from a specified file."""
        with open(token_file, "r") as file:
            data = json.load(file)
            return data.get("m2m_token")

    def get_headers(self, use_user_token=False, idempotency_key=None):
        """Generate headers for requests, including authorization and optionally idempotency key."""
        headers = {
            "Authorization": f"Bearer {self.user_token if use_user_token else self.token}",
            "Content-Type": "application/json"
        }
        if idempotency_key:
            headers["Idempotency-Key"] = idempotency_key
        return headers

    def get(self, endpoint, use_user_token=False):
        """Make a GET request to a specified endpoint."""
        headers = self.get_headers(use_user_token=use_user_token)
        response = requests.get(f"{self.base_url}{endpoint}", headers=headers)
        response.raise_for_status()
        return response.json()

    def post(self, endpoint, data, idempotency_key=None):
        """Make a POST request to a specified endpoint."""
        headers = self.get_headers(idempotency_key=idempotency_key)
        response = requests.post(f"{self.base_url}{endpoint}", headers=headers, json=data)
        response.raise_for_status()
        return response

    def create_account(self, account_data):
        """Create an account with idempotency key handling."""
        idempotency_key = str(uuid.uuid4())
        endpoint = ENDPOINTS["create_account"]
        response = self.post(endpoint, account_data, idempotency_key)

        if response.status_code == 202:
            time.sleep(2)
            response = self.post(endpoint, account_data, idempotency_key)
            if response.status_code == 201:
                return response.json()
        return response.json()

    def create_dataset(self, account_id, dataset_data):
        """Create a dataset with idempotency key handling."""
        idempotency_key = str(uuid.uuid4())
        endpoint = ENDPOINTS["create_dataset"].format(account_id=account_id)
        response = self.post(endpoint, dataset_data, idempotency_key)

        if response.status_code == 202:
            time.sleep(2)
            response = self.post(endpoint, dataset_data, idempotency_key)
            if response.status_code == 201:
                return response.json()
        return response.json()

    def get_datasets(self):
        """Get all datasets using user token."""
        endpoint = ENDPOINTS["get_datasets"]
        return self.get(endpoint, use_user_token=True)

    def get_dataset(self, dataset_id):
        """Get a specific dataset using user token."""
        endpoint = ENDPOINTS["get_dataset"].format(dataset_id=dataset_id)
        return self.get(endpoint, use_user_token=True)

    def get_application_client(self, client_id):
        """Get application client details using M2M client token."""
        endpoint = ENDPOINTS["get_application_client"].format(client_id=client_id)
        return self.get(endpoint)

    def get_dataset_servicefabric(self, dataset_id):
        """Get dataset service fabric details using user token."""
        endpoint = ENDPOINTS["get_dataset_servicefabric"].format(dataset_id=dataset_id)
        return self.get(endpoint, use_user_token=True)

    def get_users_dataset(self, dataset_id):
        """Get users associated with a dataset using user token."""
        endpoint = ENDPOINTS["get_users_dataset"].format(dataset_id=dataset_id)
        return self.get(endpoint, use_user_token=True)

    def get_users(self, user_id):
        """Get user details by user ID using user token."""
        endpoint = ENDPOINTS["get_users"].format(user_Id=user_id)
        return self.get(endpoint, use_user_token=True)

    def get_ledger_tenant(self, dataset_id):
        """Get ledger tenant details using user token."""
        endpoint = ENDPOINTS["get_ledger_tenant"].format(dataset_id=dataset_id)
        return self.get(endpoint, use_user_token=True)

    def get_query_users_dataset(self, dataset_id):
        """Query users for a dataset using user token."""
        endpoint = ENDPOINTS["get_query_users_dataset"].format(dataset_id=dataset_id)
        return self.get(endpoint, use_user_token=True)

