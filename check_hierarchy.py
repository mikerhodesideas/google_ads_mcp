#!/usr/bin/env python3
"""Check the account hierarchy."""

import os
from google.ads.googleads.client import GoogleAdsClient

# Set the credentials path
os.environ["GOOGLE_ADS_CREDENTIALS"] = os.path.expanduser("~/google-ads.yaml")

def check_account_hierarchy():
    """Check account hierarchy and permissions."""
    client = GoogleAdsClient.load_from_storage(
        os.path.expanduser("~/google-ads.yaml")
    )

    # Get all accessible accounts
    customer_service = client.get_service("CustomerService")
    accessible = customer_service.list_accessible_customers()

    accounts = [r.split("/")[-1] for r in accessible.resource_names]

    print("\nAccessible Accounts:")
    print("=" * 60)

    ga_service = client.get_service("GoogleAdsService")

    for account_id in accounts:
        print(f"\nAccount: {account_id}")

        # Try to get basic account info
        try:
            query = """
                SELECT
                    customer.id,
                    customer.descriptive_name,
                    customer.manager,
                    customer.currency_code
                FROM customer
            """

            response = ga_service.search(customer_id=account_id, query=query)

            for row in response:
                is_mcc = "MCC" if row.customer.manager else "Leaf"
                print(f"  Name: {row.customer.descriptive_name}")
                print(f"  Type: {is_mcc}")
                print(f"  Currency: {row.customer.currency_code}")

                # If it's an MCC, try to get child accounts
                if row.customer.manager:
                    child_query = """
                        SELECT
                            customer_client.id,
                            customer_client.descriptive_name
                        FROM customer_client
                        WHERE customer_client.status = 'ENABLED'
                        LIMIT 5
                    """

                    try:
                        child_response = ga_service.search(customer_id=account_id, query=child_query)
                        children = [r.customer_client.id for r in child_response]
                        print(f"  Child accounts (first 5): {', '.join(map(str, children))}")
                    except Exception as e:
                        print(f"  Could not list children: {str(e)[:80]}...")

        except Exception as e:
            print(f"  Error: {str(e)[:100]}...")

    print("\n" + "=" * 60)


if __name__ == "__main__":
    check_account_hierarchy()
