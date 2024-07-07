# my_api_project/request_bodies.py

def generate_account_body(IDfromProduct, product_Name, LoggedInUserEmail, LoggedInUserAuth0PrincipalId):
    return {
        "data": {
            "type": "Account",
            "attributes": {
                "externalId": IDfromProduct,
                "externalSource": product_Name
            },
            "relationships": {
                "owner": {
                    "data": {
                        "type": "User",
                        "attributes": {
                            "email": LoggedInUserEmail,
                            "locale": "en-GB",
                            "identityId": LoggedInUserAuth0PrincipalId
                        }
                    }
                }
            }
        }
    }

def generate_dataset_body(randomName, IDfromProduct, product_Name):
    return {
        "data": {
            "type": "Dataset",
            "attributes": {
                "name": randomName,
                "Country": "GB",
                "externalId": IDfromProduct,
                "externalSource": product_Name
            }
        }
    }
