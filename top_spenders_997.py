#!/usr/bin/env python3
"""Find top spending accounts in the last 30 days under the 997 MCC."""

import os
from datetime import datetime, timedelta
from google.ads.googleads.client import GoogleAdsClient
import yaml

def get_top_spenders_997(days=30, limit=10):
    """Get top spending accounts under the 997 MCC."""

    # Load the yaml and temporarily override login_customer_id
    yaml_path = os.path.expanduser("~/google-ads.yaml")

    with open(yaml_path, 'r') as f:
        config = yaml.safe_load(f)

    # Override the login_customer_id to use the 997 MCC
    config['login_customer_id'] = '9978959108'

    # Create client with updated config
    client = GoogleAdsClient.load_from_dict(config)

    mcc_id = "9978959108"

    print(f"\nTop 10 Accounts by Spend (Last 30 Days)")
    print(f"MCC Account: {mcc_id}")
    print("=" * 80)

    ga_service = client.get_service("GoogleAdsService")

    # Get all child accounts
    child_query = """
        SELECT
            customer_client.id,
            customer_client.descriptive_name,
            customer_client.currency_code,
            customer_client.status
        FROM customer_client
        WHERE customer_client.status = 'ENABLED'
    """

    try:
        response = ga_service.search(customer_id=mcc_id, query=child_query)

        child_accounts = []
        for row in response:
            child_accounts.append({
                'id': str(row.customer_client.id),
                'name': row.customer_client.descriptive_name,
                'currency': row.customer_client.currency_code
            })

        print(f"\nFound {len(child_accounts)} enabled child accounts\n")

        if not child_accounts:
            print("No child accounts found")
            return

    except Exception as e:
        print(f"Error getting child accounts: {e}")
        return

    # Get spend for each account
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    start_date_str = start_date.strftime("%Y-%m-%d")
    end_date_str = end_date.strftime("%Y-%m-%d")

    accounts_with_spend = []

    for account in child_accounts:
        customer_id = account['id']

        try:
            spend_query = f"""
                SELECT
                    metrics.cost_micros
                FROM customer
                WHERE segments.date BETWEEN '{start_date_str}' AND '{end_date_str}'
            """

            spend_response = ga_service.search(customer_id=customer_id, query=spend_query)

            total_cost_micros = 0
            for row in spend_response:
                total_cost_micros += row.metrics.cost_micros

            cost = total_cost_micros / 1_000_000

            accounts_with_spend.append({
                'customer_id': customer_id,
                'name': account['name'],
                'currency': account['currency'],
                'cost': cost
            })

        except Exception as e:
            print(f"Error getting spend for {customer_id}: {str(e)[:80]}...")
            accounts_with_spend.append({
                'customer_id': customer_id,
                'name': account['name'],
                'currency': account['currency'],
                'cost': 0
            })

    # Sort by spend descending
    accounts_with_spend.sort(key=lambda x: x['cost'], reverse=True)

    # Show top 10
    top_accounts = accounts_with_spend[:limit]

    print(f"{'Rank':<6}{'Customer ID':<15}{'Name':<40}{'Currency':<10}{'Spend':<15}")
    print("-" * 90)

    for i, account in enumerate(top_accounts, 1):
        print(f"{i:<6}{account['customer_id']:<15}{account['name'][:38]:<40}"
              f"{account['currency']:<10}{account['cost']:>14,.2f}")

    print("-" * 90)
    total_spend = sum(acc['cost'] for acc in top_accounts)
    currency = top_accounts[0]['currency'] if top_accounts else 'N/A'
    print(f"{'Total:':<61}{currency:<10}{total_spend:>14,.2f}")
    print()


if __name__ == "__main__":
    get_top_spenders_997()
