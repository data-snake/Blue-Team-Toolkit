#!/usr/bin/env python3
"""
windows_event_parser.py - Parse Windows EVTX log file into JSON output.
"""
import argparse
import json
from Evtx.Evtx import Evtx


def parse_evtx(file_path):
    """
    Read an EVTX log file and return a list of XML strings for each record.
    """
    records = []
    with Evtx(file_path) as log:
        for record in log.records():
            records.append(record.xml())
    return records


def main():
    parser = argparse.ArgumentParser(description='Windows Event Log Parser')
    parser.add_argument('evtx', help='Path to the .evtx file')
    parser.add_argument('-o', '--output', help='Write JSON output to file')
    args = parser.parse_args()

    events = parse_evtx(args.evtx)

    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(events, f, ensure_ascii=False, indent=2)
        print(f"Written {len(events)} events to {args.output}")
    else:
        print(json.dumps(events, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
