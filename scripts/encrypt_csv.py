"""Small helper: encrypt the CSV file using Fernet and write .enc file.

Usage:
    python scripts/encrypt_csv.py --in src/utils/COMPLETO.csv --out src/utils/COMPLETO.csv.enc

It prints the base64 key to stdout; store it securely (DO NOT commit it).
"""
import argparse
import os
import sys

# Ensure the project's src/ directory is on sys.path so imports work when running
# the script from the repository root (or other working directories).
PROJ_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
SRC_DIR = os.path.join(PROJ_ROOT, 'src')
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

from utils.crypto import generate_key, encrypt_file


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--in', dest='infile', required=True)
    p.add_argument('--out', dest='outfile', required=False)
    args = p.parse_args()

    infile = args.infile
    outfile = args.outfile or infile + '.enc'

    if not os.path.exists(infile):
        print('Input file not found:', infile)
        return

    key = generate_key()
    encrypt_file(infile, outfile, key)
    print('Encrypted written to', outfile)
    print('Keep this KEY safe and set as environment variable CSV_ENC_KEY')
    print(key.decode())

if __name__ == '__main__':
    main()
