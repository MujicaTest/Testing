# sageid_auth.py

import requests
import base64
import json
from bs4 import BeautifulSoup
import secrets
import hashlib
import urllib.parse
import argparse
import logging

class SageIDAuthAutomation:

    def __init__(self, client_id, redirect_uri, scope, audience, username, password, verbose):

        self.client_id = client_id
        self.redirect_uri = redirect_uri
        self.scope = scope
        self.audience = audience
        self.username = username
        self.password = password
        self.verbose = verbose

        logging.basicConfig(level=logging.DEBUG if self.verbose else logging.INFO)
        self.logger = logging.getLogger(__name__)

        self.headers = {
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7'
        }

        self.shadow_usernamepassword_challenge_endpoint = "https://id-shadow.sage.com/usernamepassword/challenge"
        self.shadow_usernamepassword_login_endpoint = "https://id-shadow.sage.com/usernamepassword/login"
        self.shadow_login_callback_endpoint = "https://id-shadow.sage.com/login/callback"
        self.shadow_oauth_token_endpoint = "https://id-shadow.sage.com/oauth/token"
        
        self.session = requests.Session()
        self.login_state = None
        self._csrf = None
        self.code_verifier = self.generate_code_verifier()
        self.code_challenge = self.generate_code_challenge(self.code_verifier)
        self.url_params = "client_id=" + self.client_id + "&scope=" + urllib.parse.quote_plus(self.scope) + "&redirect_uri="+ urllib.parse.quote_plus(self.redirect_uri) + "&audience=" + urllib.parse.quote_plus(self.audience) + "&response_type=code&response_mode=query&state=SWMwV0pYdExsRUUwaW53VFN1bjZuU3JQaDlaR3BuQUxwcmJoTWlBbl90eA%3D%3D&nonce=TzBGbXZ6Q3JYWFVobkZMVzFaZ1l0LXYxbVZweVozc0M3N21mS0Z5R0lXcQ%3D%3D&code_challenge=" + self.code_challenge + "&code_challenge_method=S256&auth0Client=eyJuYW1lIjoiYXV0aDAtcmVhY3QiLCJ2ZXJzaW9uIjoiMi4yLjQifQ%3D%3D"

        self.debug_output = False

    def get_access_token(self):
        """Obtains the access token by setting up authentication and retrieving OAuth token data."""
        self.auth_setup()
        token_data = self.get_oauth_token_data()
        
        # Save the token to a file
        with open("user_token.json", "w") as file:
            json.dump({"token": token_data['access_token']}, file)
        
        return token_data['access_token']

    def auth_setup(self):
        """Sets up the authentication process by performing necessary HTTP requests."""
        authorize = self.session.get("https://id-shadow.sage.com/authorize?"+self.url_params, allow_redirects=True)
        login_redirect = authorize.url

        self.login_state = self.get_url_param(login_redirect.split("?")[1].split("&"), "state")
        self.logger.debug("Login State: " + self.login_state)
        login = self.session.get(login_redirect, headers=self.headers)
        self._csrf = json.loads(base64.b64decode(str(login.content).split("encodedAuth0Config=")[1].split("\"")[1]))['extraParams']['_csrf']
        self.logger.debug("CSRF: " + self._csrf)

    def get_oauth_token_data(self):
        """Fetches OAuth token data by following a series of steps involving HTTP requests."""
        challenge = self.session.post(self.shadow_usernamepassword_challenge_endpoint, json={"state": self.login_state})
        self.logger.debug("usernamepassword/challenge: " + str(challenge.status_code))

        login_data = {
            "auth_client": self.client_id,
            "code_challenge": self.code_challenge,
            "code_challenge_method": "S256",
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "tenant": "sage-cid-shadow",
            "response_type": "code",
            "response_mode": "query",
            "scope": self.scope,
            "state": self.login_state,
            "nonce": "WWhOaUZBYVpmOGVQeWFnT2tFc1JWM1NiSHMtdzVIVEppQm40MjNQT28wQw==",
            "connection": "CloudID",
            "username": self.username,
            "password": self.password,
            "popup_options": {},
            "sso": True,
            "protocol": "oauth2",
            "_csrf": self._csrf,
            "_instate": "deprecated",
            "audience": self.audience
        }

        login_data = self.session.post(self.shadow_usernamepassword_login_endpoint, json=login_data, allow_redirects=True)
        self.logger.debug("usernamepassword/login: " + str(login_data.status_code))

        html = BeautifulSoup(login_data.text, features="lxml")
        wresult = html.find('input', {'name':'wresult'})['value']
        wctx = html.find('input', {'name':'wctx'})['value']

        self.logger.debug("wresult: " + wresult)
        self.logger.debug("wctx:" + wctx)

        login_callback_data = {
            "wctx": wctx,
            "wresult": wresult,
            "wa": "wsignin1.0"
        }

        callback = self.session.post(self.shadow_login_callback_endpoint, json=login_callback_data)
        self.logger.debug("login/callback: " + str(callback.status_code))

        for url in callback.history:
            self.logger.debug("Callback History URL: " + url.url)
            if("code" in str(url.content)):
                code = (str(url.content).split("code=")[1].split("&")[0])

        auth_token_post = {
            "client_id": self.client_id,
            "code_verifier": self.code_verifier,
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": self.redirect_uri
        }

        oauth_token = self.session.post(self.shadow_oauth_token_endpoint, json=auth_token_post)
        self.logger.debug("oauth/token: " + str(oauth_token.status_code))

        self.logger.debug("Received OAuth Token: " + str(oauth_token.json()))
        return oauth_token.json()

    def get_url_param(self, params, id):
        """Extracts a parameter value from a list of URL parameters."""
        for param in params:
            if id in param:
                return param.split("=")[1]

    def generate_code_verifier(self, length=128):
        """Generates a code verifier for OAuth2 PKCE (Proof Key for Code Exchange) flow."""
        return secrets.token_urlsafe(length)

    def generate_code_challenge(self, code_verifier):
        """Generates a code challenge from a code verifier for OAuth2 PKCE (Proof Key for Code Exchange) flow."""
        code_challenge = hashlib.sha256(code_verifier.encode()).digest()
        return base64.urlsafe_b64encode(code_challenge).decode().rstrip("=")

def print_help():
    print("Usage: python sageid_auth.py [options]")
    print("  ! Please ensure dependencies are installed !")
    print("  ! Confirmed to work with Python3.11 !")
    print("Options:")
    print("  --client-id      Client ID (required)")
    print("  --redirect_uri   Redirect URI (required)")
    print("  --scope          Scope (required)")
    print("  --audience       Audience (required)")
    print("  --username       Username (required)")
    print("  --password       Password (required)")
    print("  --verbose        Enable verbose mode to get a complete call trace for the authentication.")
    print("  --help           Show this message.")

def main():
    parser = argparse.ArgumentParser(description="SageID Command Line Automation Tool", add_help=False)
    
    parser.add_argument("--client-id", required=False)
    parser.add_argument("--redirect_uri",  required=False)
    parser.add_argument("--scope",  required=False)
    parser.add_argument("--audience", required=False)
    parser.add_argument("--username", required=False)
    parser.add_argument("--password",  required=False)
    parser.add_argument("--verbose", action="store_true")
    parser.add_argument("--help", action="store_true")


    args = parser.parse_args()
    if(args.help or args.client_id is None