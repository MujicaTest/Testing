# my_api_project/config.py

class Config:
    ENVIRONMENTS = {
        "qa02": "https://7b5klike76.execute-api.eu-west-1.amazonaws.com",
        "qa01": "https://qa01-api.nas-eng.sage.com",
        "int": "https://int-api.nas-eng.sage.com",
        "pp": "https://api-pp.example.com", # when The first test run well in the previous env I will update this
        "SBX": "https://api-sbx.example.com", # when The first test run well in the previous env I will update this
        "Prod": "https://api-prod.example.com" # when The first test run well in the previous env I will update this
    }

    @classmethod
    def get_base_url(cls, environment):
        return cls.ENVIRONMENTS.get(environment, None)

# Define the endpoints
ENDPOINTS = {
    "create_account": "/accounts",
    "create_dataset": "/accounts/{account_id}/datasets"
}
