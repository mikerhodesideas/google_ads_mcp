#!/usr/bin/env python3
"""Find top spending accounts in the last 30 days for CIDs starting with 997."""

import os
from datetime import datetime, timedelta
from google.ads.googleads.client import GoogleAdsClient

# Set the credentials path
os.environ["GOOGLE_ADS_CREDENTIALS"] = os.path.expanduser("~/google-ads.yaml")

def get_child_accounts(client, mcc_id, prefix="997"):
    """Get all child accounts under an MCC that match the prefix."""
    ga_service = client.get_service("GoogleAdsService")

    query = """
        SELECT
            customer_client.id,
            customer_client.descriptive_name,
            customer_client.currency_code,
            customer_client.status
        FROM customer_client
        WHERE customer_client.status = 'ENABLED'
    """

    try:
        response = ga_service.search(customer_id=mcc_id, query=query)

        accounts = []
        for row in response:
            customer_id = str(row.customer_client.id)
            if customer_id.startswith(prefix):
                accounts.append({
                    'id': customer_id,
                    'name': row.customer_client.descriptive_name,
                    'currency': row.customer_client.currency_code
                })

        return accounts

    except Exception as e:
        print(f"Error getting child accounts: {e}")
        return []


def get_account_spend(client, mcc_id, customer_id, days=30):
    """Get spend for a specific account."""
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)

    start_date_str = start_date.strftime("%Y-%m-%d")
    end_date_str = end_date.strftime("%Y-%m-%d")

    ga_service = client.get_service("GoogleAdsService")

    query = f"""
        SELECT
            metrics.cost_micros
        FROM customer
        WHERE segments.date BETWEEN '{start_date_str}' AND '{end_date_str}'
    """

    try:
        response = ga_service.search(customer_id=customer_id, query=query)

        total_cost = 0
        for row in response:
            total_cost += row.metrics.cost_micros

        return total_cost / 1_000_000  # Convert to currency units

    except Exception as e:
        print(f"Error getting spend for {customer_id}: {e}")
        return 0


def main():
    """Main function."""
    # The account starting with 997
    target_mcc = "9978959108"

    client = GoogleAdsClient.load_from_storage(
        os.path.expanduser("~/google-ads.yaml")
    )

    print(f"\nTop 10 Accounts by Spend (Last 30 Days)")
    print(f"Checking MCC Account: {target_mcc}")
    print("=" * 80)

    # Get all child accounts under the 997 MCC
    child_accounts = get_child_accounts(client, target_mcc, prefix="")

    if not child_accounts:
        print(f"No child accounts found under {target_mcc}")
        print("This might be a leaf account (not an MCC), or it has no active child accounts.")
        return

    print(f"\nFound {len(child_accounts)} enabled child accounts\n")

    # Get spend for each account
    accounts_with_spend = []
    for account in child_accounts:
        spend = get_account_spend(client, mcc_id, account['id'], days=30)
        accounts_with_spend.append({
            'customer_id': account['id'],
            'name': account['name'],
            'currency': account['currency'],
            'cost': spend
        })

    # Sort by spend descending
    accounts_with_spend.sort(key=lambda x: x['cost'], reverse=True)

    # Show top 10
    top_accounts = accounts_with_spend[:10]

    print(f"{'Rank':<6}{'Customer ID':<15}{'Name':<30}{'Currency':<10}{'Spend':<15}")
    print("-" * 80)

    for i, account in enumerate(top_accounts, 1):
        print(f"{i:<6}{account['customer_id']:<15}{account['name']:<30}"
              f"{account['currency']:<10}{account['cost']:>14,.2f}")

    print("-" * 80)
    total_spend = sum(acc['cost'] for acc in top_accounts)
    currency = top_accounts[0]['currency'] if top_accounts else 'N/A'
    print(f"{'Total:':<51}{currency:<10}{total_spend:>14,.2f}")
    print()


if __name__ == "__main__":
    main()
