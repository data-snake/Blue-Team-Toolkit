#!/usr/bin/env python3
"""
apache_parser.py - Parse Apache access logs (Common Log Format) and output JSON.
"""
import re
import json
import argparse

# Regex for Common Log Format: host ident authuser [date] "request" status bytes
LOG_PATTERN = re.compile(
    r'(?P<host>\S+) \S+ \S+ \[(?P<time>[^\]]+)\] "(?P<request>[^"]+)" (?P<status>\d{3}) (?P<size>\S+)'
)

def parse_line(line):
    match = LOG_PATTERN.match(line)
    if not match:
        return None
    data = match.groupdict()
    data['status'] = int(data['status'])
    data['size'] = int(data['size']) if data['size'].isdigit() else 0
    return data


def main():
    parser = argparse.ArgumentParser(description='Parse Apache logs to JSON')
    parser.add_argument('logfile', help='Path to Apache access log')
    parser.add_argument('-o', '--output', help='Write output to JSON file')
    args = parser.parse_args()
    results = []

    with open(args.logfile, 'r') as f:
        for line in f:
            parsed = parse_line(line)
            if parsed:
                results.append(parsed)

    if args.output:
        with open(args.output, 'w') as out:
            json.dump(results, out, indent=2)
        print(f"Written {len(results)} entries to {args.output}")
    else:
        print(json.dumps(results, indent=2))

if __name__ == '__main__':
    main()