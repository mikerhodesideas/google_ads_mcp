#!/usr/bin/env python3
"""List all accessible Google Ads accounts."""

import os
from google.ads.googleads.client import GoogleAdsClient

# Set the credentials path
os.environ["GOOGLE_ADS_CREDENTIALS"] = os.path.expanduser("~/google-ads.yaml")

def list_accounts():
    """List all accessible Google Ads accounts."""
    client = GoogleAdsClient.load_from_storage(
        os.path.expanduser("~/google-ads.yaml")
    )

    customer_service = client.get_service("CustomerService")

    # Get accessible customers
    accessible_customers = customer_service.list_accessible_customers()

    print("\nAccessible Google Ads Accounts:")
    print("=" * 60)

    resource_names = accessible_customers.resource_names

    if not resource_names:
        print("No accessible accounts found.")
        return

    # Extract customer IDs from resource names
    for resource_name in resource_names:
        customer_id = resource_name.split("/")[-1]
        print(f"Customer ID: {customer_id}")

    print("=" * 60)
    print(f"\nTotal accounts: {len(resource_names)}")

if __name__ == "__main__":
    list_accounts()
