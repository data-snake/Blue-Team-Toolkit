#!/usr/bin/env python3
"""
hash_checker.py - Compute MD5, SHA1, and SHA256 hashes for a given file.
"""
import hashlib
import argparse

def compute_hashes(file_path):
    """
    Read the file at file_path in binary mode and compute MD5, SHA1, and SHA256 digests.
    Returns a dict mapping algorithm names to hex digests.
    """
    with open(file_path, 'rb') as f:
        data = f.read()

    return {
        'MD5': hashlib.md5(data).hexdigest(),
        'SHA1': hashlib.sha1(data).hexdigest(),
        'SHA256': hashlib.sha256(data).hexdigest(),
    }

def main():
    parser = argparse.ArgumentParser(
        description='Compute MD5, SHA1, and SHA256 hashes for a file.'
    )
    parser.add_argument(
        'file',
        help='Path to the file to hash'
    )
    args = parser.parse_args()

    try:
        hashes = compute_hashes(args.file)
        for algo, digest in hashes.items():
            print(f"{algo}: {digest}")
    except FileNotFoundError:
        print(f"Error: File not found: {args.file}")
    except PermissionError:
        print(f"Error: Permission denied when accessing: {args.file}")
    except Exception as e:
        print(f"Unexpected error computing hashes: {e}")

if __name__ == '__main__':
    main()
