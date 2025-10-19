#!/usr/bin/env python3
"""Get campaign performance for Kip&Co."""

import os
from datetime import datetime, timedelta
from google.ads.googleads.client import GoogleAdsClient
import yaml

def get_campaign_performance(customer_id, login_customer_id, days=60):
    """Get campaign performance for a specific account."""

    # Load the yaml and set login_customer_id
    yaml_path = os.path.expanduser("~/google-ads.yaml")

    with open(yaml_path, 'r') as f:
        config = yaml.safe_load(f)

    config['login_customer_id'] = login_customer_id

    # Create client with updated config
    client = GoogleAdsClient.load_from_dict(config)

    # Calculate date range
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    start_date_str = start_date.strftime("%Y-%m-%d")
    end_date_str = end_date.strftime("%Y-%m-%d")

    ga_service = client.get_service("GoogleAdsService")

    query = f"""
        SELECT
            campaign.id,
            campaign.name,
            campaign.status,
            metrics.cost_micros,
            metrics.impressions,
            metrics.clicks,
            metrics.conversions,
            metrics.conversions_value
        FROM campaign
        WHERE segments.date BETWEEN '{start_date_str}' AND '{end_date_str}'
        ORDER BY metrics.cost_micros DESC
    """

    try:
        response = ga_service.search(customer_id=customer_id, query=query)

        campaigns = {}
        for row in response:
            campaign_id = row.campaign.id
            if campaign_id not in campaigns:
                campaigns[campaign_id] = {
                    'id': campaign_id,
                    'name': row.campaign.name,
                    'status': row.campaign.status.name,
                    'cost': 0,
                    'impressions': 0,
                    'clicks': 0,
                    'conversions': 0,
                    'conv_value': 0
                }

            campaigns[campaign_id]['cost'] += row.metrics.cost_micros / 1_000_000
            campaigns[campaign_id]['impressions'] += row.metrics.impressions
            campaigns[campaign_id]['clicks'] += row.metrics.clicks
            campaigns[campaign_id]['conversions'] += row.metrics.conversions
            campaigns[campaign_id]['conv_value'] += row.metrics.conversions_value

        # Convert to list and sort by cost
        campaign_list = list(campaigns.values())
        campaign_list.sort(key=lambda x: x['cost'], reverse=True)

        return campaign_list

    except Exception as e:
        print(f"Error getting campaign data: {e}")
        return []


if __name__ == "__main__":
    # Kip&Co
    customer_id = "4779792239"
    login_customer_id = "9978959108"  # WebSavvy MCC

    print(f"\nCampaign Performance - Last 60 Days")
    print(f"Account: Kip&Co ({customer_id})")
    print("=" * 130)

    campaigns = get_campaign_performance(customer_id, login_customer_id, days=60)

    if not campaigns:
        print("No campaign data found")
    else:
        print(f"\n{'Campaign Name':<50}{'Status':<12}{'Spend':<15}{'Clicks':<10}{'Impr.':<12}{'Conv.':<10}{'Conv. Val':<15}")
        print("-" * 130)

        total_spend = 0
        total_clicks = 0
        total_impressions = 0
        total_conversions = 0
        total_conv_value = 0

        for campaign in campaigns:
            ctr = (campaign['clicks'] / campaign['impressions'] * 100) if campaign['impressions'] > 0 else 0
            roas = (campaign['conv_value'] / campaign['cost']) if campaign['cost'] > 0 else 0

            print(f"{campaign['name'][:48]:<50}"
                  f"{campaign['status']:<12}"
                  f"${campaign['cost']:>13,.2f}"
                  f"{campaign['clicks']:>10,}"
                  f"{campaign['impressions']:>12,}"
                  f"{campaign['conversions']:>10.1f}"
                  f"${campaign['conv_value']:>13,.2f}")

            total_spend += campaign['cost']
            total_clicks += campaign['clicks']
            total_impressions += campaign['impressions']
            total_conversions += campaign['conversions']
            total_conv_value += campaign['conv_value']

        print("-" * 130)
        overall_ctr = (total_clicks / total_impressions * 100) if total_impressions > 0 else 0
        overall_roas = (total_conv_value / total_spend) if total_spend > 0 else 0

        print(f"{'TOTAL':<50}{'':12}"
              f"${total_spend:>13,.2f}"
              f"{total_clicks:>10,}"
              f"{total_impressions:>12,}"
              f"{total_conversions:>10.1f}"
              f"${total_conv_value:>13,.2f}")

        print(f"\nOverall CTR: {overall_ctr:.2f}% | Overall ROAS: {overall_roas:.2f}x")
        print()
