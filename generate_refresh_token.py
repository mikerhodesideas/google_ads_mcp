#!/usr/bin/env python3
"""Generates a refresh token for Google Ads API using OAuth2."""

import os
import sys
import yaml
from google_auth_oauthlib.flow import InstalledAppFlow

# OAuth2 scopes for Google Ads API
SCOPES = ["https://www.googleapis.com/auth/adwords"]

def main():
    """Generate and display the refresh token."""

    # Load credentials from yaml file
    yaml_path = os.path.expanduser("~/google-ads.yaml")

    if not os.path.exists(yaml_path):
        print(f"Error: {yaml_path} not found")
        print("Please create the file with client_id and client_secret")
        sys.exit(1)

    with open(yaml_path, 'r') as f:
        config = yaml.safe_load(f)

    client_id = config.get('client_id')
    client_secret = config.get('client_secret')

    if not client_id or not client_secret:
        print("Error: client_id and client_secret must be in ~/google-ads.yaml")
        sys.exit(1)

    client_config = {
        "installed": {
            "client_id": client_id,
            "client_secret": client_secret,
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
        }
    }

    flow = InstalledAppFlow.from_client_config(
        client_config,
        scopes=SCOPES
    )

    # Run the OAuth flow
    credentials = flow.run_local_server(port=0)

    print("\n" + "="*60)
    print("SUCCESS! Your refresh token:")
    print("="*60)
    print(credentials.refresh_token)
    print("="*60)
    print("\nSave this token securely!")

if __name__ == "__main__":
    main()
