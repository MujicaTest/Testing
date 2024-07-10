# POC_APItest/api_client.py
import requests
import json
import uuid
from config import Config, ENDPOINTS

class APIClient:
    def __init__(self, environment, token_file="token.json"):
        self.base_url = Config.get_base_url(environment)
        if not self.base_url:
            raise ValueError(f"Invalid environment: {environment}")
        self.token = self._read_token(token_file)

    def _read_token(self, token_file):
        with open(token_file, "r") as file:
            data = json.load(file)
            return data.get("token")

    def get_headers(self, idempotency_key=None):
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
        if idempotency_key:
            headers["Idempotency-Key"] = idempotency_key
        return headers

    def post(self, endpoint, data, idempotency_key=None):
        headers = self.get_headers(idempotency_key)
        response = requests.post(f"{self.base_url}/{endpoint}", headers=headers, json=data)
        response.raise_for_status()
        return response.json()

    def create_account(self, account_data):
        idempotency_key = str(uuid.uuid())
        endpoint = ENDPOINTS["create_account"]
        return self.post(endpoint, account_data, idempotency_key)

    def create_dataset(self, account_id, dataset_data):
        idempotency_key = str(uuid.uuid1())
        endpoint = ENDPOINTS["create_dataset"].format(account_id=account_id)
        return self.post(endpoint, dataset_data, idempotency_key)
    
    def get_datasetId(self, dataset_id):
        endpoint = ENDPOINTS["get_dataset_id"].format(dataset_id=)
        return self.post(endpoint, dataset_data)
