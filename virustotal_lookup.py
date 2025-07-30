#!/usr/bin/env python3
"""
virustotal_lookup.py - Query VirusTotal for file, IP, or domain indicators.
"""
import os
import sys
import argparse
import requests
import json

API_KEY = os.getenv('VIRUSTOTAL_API_KEY')
if not API_KEY:
    print("Error: Set VIRUSTOTAL_API_KEY environment variable.")
    sys.exit(1)

BASE_URL = "https://www.virustotal.com/api/v3"

def lookup(indicator, itype):
    url = f"{BASE_URL}/{itype}s/{indicator}"
    headers = {'x-apikey': API_KEY}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()


def main():
    parser = argparse.ArgumentParser(description='VirusTotal IOC Lookup')
    parser.add_argument('indicator', help='Hash, IP, or domain')
    parser.add_argument('-t', '--type', choices=['file', 'ip', 'domain'], default='file')
    parser.add_argument('-o', '--output', help='Output JSON file')
    args = parser.parse_args()

    try:
        result = lookup(args.indicator, args.type)
        data = json.dumps(result, indent=2)
        if args.output:
            with open(args.output, 'w') as f:
                f.write(data)
            print(f"Written output to {args.output}")
        else:
            print(data)
    except requests.HTTPError as e:
        print(f"HTTPError: {e}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    main()
