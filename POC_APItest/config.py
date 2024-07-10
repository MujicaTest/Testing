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
    "create_account": "/accounts",#Use m2m client
    "create_dataset": "/accounts/{account_id}/datasets",#Use m2m client
    "get_application_client":"/application/clients/{client_id}", #Use m2m client
    "get_datasets": "/datasets", #Use user token
    "get_dataset_id" : "/datasets/{dataset_id}",#Use user token
    "get_dataset_id_servicefabric" : "/datasets/{dataset_id}?include=servicefabric", #Use user token
    "get_users_dataset" : "/datasets/{dataset_id}/users", #GET Query users for a dataset - Use user token
    "get_users" : "/users/{user_Id}",# you need already to know the ID of the user to perform this endpoint - Use user token
    "get_ledger_tenant" : "/datasets/{dataset_id}/ledger-service-tenant",#Use user token - the dataset already be fixed in org service with this value
}
