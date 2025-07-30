#!/usr/bin/env python3
"""
ip_reputation_check.py - Check IP reputation using AbuseIPDB API.
"""
import os
import sys
import argparse
import requests
import json

API_KEY = os.getenv('ABUSEIPDB_API_KEY')
if not API_KEY:
    print("Error: Set ABUSEIPDB_API_KEY environment variable.")
    sys.exit(1)

API_URL = 'https://api.abuseipdb.com/api/v2/check'


def check_ip_reputation(ip_address, days):
    params = {
        'ipAddress': ip_address,
        'maxAgeInDays': days
    }
    headers = {
        'Key': API_KEY,
        'Accept': 'application/json'
    }
    response = requests.get(API_URL, headers=headers, params=params)
    response.raise_for_status()
    return response.json()


def main():
    parser = argparse.ArgumentParser(description='Check IP reputation via AbuseIPDB')
    parser.add_argument('ip', help='IP address to check')
    parser.add_argument('-d', '--days', type=int, default=90,
                        help='Max age of reports in days (default: 90)')
    parser.add_argument('-o', '--output', help='Save JSON output to file')
    args = parser.parse_args()

    try:
        result = check_ip_reputation(args.ip, args.days)
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2)
            print(f"Written output to {args.output}")
        else:
            print(json.dumps(result, indent=2))
    except requests.HTTPError as e:
        print(f"HTTPError: {e}")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == '__main__':
    main()
