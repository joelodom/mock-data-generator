#!/usr/bin/env python3
import csv
import sys
import random
import string

def clean_field(s):
    """Turn any Unicode replacement char into a plain '?'."""
    return s.replace('\ufffd', '?')

def read_voter_file(filepath):
    """
    Reads a quoted, tab‑delimited voter file into:
      - headers: a list of column names (from the first row)
      - records: a list of dicts mapping header -> cleaned value
    Any undecodable byte is first mapped to '�' then turned into '?'.
    """
    with open(filepath, newline='', encoding='ascii', errors='replace') as f:
        reader = csv.reader(f, delimiter='\t', quotechar='"')
        # Read and clean headers
        raw_headers = next(reader)
        headers = [clean_field(h) for h in raw_headers]

        # Read, clean, and zip each row
        records = []
        for row in reader:
            clean_row = [clean_field(cell) for cell in row]
            # In case some rows have fewer/more fields, zip only up to min length
            rec = {h: clean_row[i] for i, h in enumerate(headers) if i < len(clean_row)}
            records.append(rec)

    return headers, records

def fakeCCNumber():
    """
    Generate a fake credit card number in the format 0000-0000-0000-0000.
    """
    # Create four groups of four digits each, zero-padded
    groups = [f"{random.randint(0, 9999):04d}" for _ in range(4)]
    # Join with hyphens
    return "-".join(groups)


def fakeSSN():
    """
    Generate a fake Social Security number in the format XXX-XX-XXXX.
    """
    # Create the three parts: 3 digits, 2 digits, and 4 digits
    part1 = f"{random.randint(0, 999):03d}"
    part2 = f"{random.randint(0, 99):02d}"
    part3 = f"{random.randint(0, 9999):04d}"
    return f"{part1}-{part2}-{part3}"



def fakeLicensePlate():
    """
    Generate a fake license plate number in the format AAA-0000.
    """
    # Three uppercase letters
    letters = ''.join(random.choice(string.ascii_uppercase) for _ in range(3))
    # Four digits
    numbers = ''.join(random.choice(string.digits) for _ in range(4))
    return f"{letters} {numbers}"


# Generate a static list of 100 unique fake procedure codes at import time
_PROCEDURE_CODES = [
    f"{code:05d}"
    for code in random.sample(range(0, 100_000), 100)
]

def fakeProcedureCode():
    """
    Return a fake medical procedure code (CPT-style five-digit string),
    chosen from a pre-defined set of ~100 codes.
    """
    return random.choice(_PROCEDURE_CODES)





# Common free‐email providers with weights
COMMON_DOMAINS = ["gmail.com", "yahoo.com", "outlook.com", "hotmail.com"]
COMMON_WEIGHTS = [40, 15, 10, 5]

# How to mix domain types: common providers, company‐style, and random
DOMAIN_SOURCES = ["common", "company", "random"]
DOMAIN_SOURCE_WEIGHTS = [70, 15, 15]  # sum to 100

# TLDs for generated domains
TLDs = ["com", "net", "org", "io", "co", "biz", "info"]

def pronounceable_word(min_len=3, max_len=8):
    """Generate an alternating consonant‐vowel string to mimic a pronounceable word."""
    vowels = "aeiou"
    consonants = "".join(set(string.ascii_lowercase) - set(vowels))
    length = random.randint(min_len, max_len)
    start_with_consonant = random.random() < 0.8
    word = []
    for i in range(length):
        if start_with_consonant:
            word.append(consonants if i % 2 == 0 else vowels)
        else:
            word.append(vowels if i % 2 == 0 else consonants)
        # pick a random character from that set
        word[-1] = random.choice(word[-1])
    return "".join(word)

def _generate_company_domain():
    """Make a plausible company‐style domain (pronounceable label + TLD)."""
    label = pronounceable_word(5, 10)
    tld = random.choice(TLDs)
    return f"{label}.{tld}"

def _generate_random_domain():
    """Make a random‐letters domain + TLD."""
    length = random.randint(5, 10)
    label = "".join(random.choice(string.ascii_lowercase) for _ in range(length))
    tld = random.choice(TLDs)
    return f"{label}.{tld}"

def fakeEmailAddress():
    """
    Generate a fake email address:
      - ~1 in 50 will be VERY long (100–254 chars total).
      - Otherwise, ~60% are 'realistic' patterns (first.last, initials, etc.),
        ~40% purely random local parts.
      - Domains mix common providers, company‐style, and random domains.
    """
    # 1-in-50 chance of a long address
    if random.randint(1, 50) == 1:
        # pick domain source
        src = random.choices(DOMAIN_SOURCES, weights=DOMAIN_SOURCE_WEIGHTS, k=1)[0]
        if src == "common":
            domain = random.choices(COMMON_DOMAINS, weights=COMMON_WEIGHTS, k=1)[0]
        elif src == "company":
            domain = _generate_company_domain()
        else:
            domain = _generate_random_domain()

        total_length = random.randint(100, 254)
        local_length = total_length - len(domain) - 1  # minus '@'
        alphabet = string.ascii_lowercase + string.digits
        # random alphanumeric local part
        local = "".join(random.choice(alphabet) for _ in range(local_length))
        return f"{local}@{domain}"

    # NORMAL‐LENGTH ADDRESS
    # decide local‐part style
    if random.random() < 0.6:
        # pronounceable first+last patterns
        first = pronounceable_word(3, 7)
        last = pronounceable_word(3, 8)
        patterns = [
            f"{first}.{last}",
            f"{first}{last}",
            f"{first[0]}{last}",
            f"{first}_{last}",
            f"{first}{random.randint(1, 99)}",
            f"{last}{random.randint(1, 999)}"
        ]
        local = random.choice(patterns)
    else:
        # random local part with common allowed chars
        chars = string.ascii_lowercase + string.digits + "._%+-"
        length = random.randint(1, 20)
        local = "".join(random.choice(chars) for _ in range(length))

    # pick domain
    src = random.choices(DOMAIN_SOURCES, weights=DOMAIN_SOURCE_WEIGHTS, k=1)[0]
    if src == "common":
        domain = random.choices(COMMON_DOMAINS, weights=COMMON_WEIGHTS, k=1)[0]
    elif src == "company":
        domain = _generate_company_domain()
    else:
        domain = _generate_random_domain()

    return f"{local}@{domain}"









def main():
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} path/to/voter_data.tsv", file=sys.stderr)
        sys.exit(1)

    filepath = sys.argv[1]
    try:
        headers, records = read_voter_file(filepath)
    except Exception as e:
        print(f"Error reading {filepath!r}: {e}", file=sys.stderr)
        sys.exit(1)

    print(f"Loaded {len(records)} records with {len(headers)} fields each.\n")
    print("Fields:")
    for h in headers:
        print(f"  • {h}")
    if records:
        print("\nFirst record preview:")
        for k, v in records[0].items():
            print(f"  {k!r}: {v!r}")
    
    for record in records:
        print(f"{record["first_name"]} {record["last_name"]}")
        print(f"{record["mail_addr1"]}")
        print(f"{record["mail_city"]}, {record["mail_state"]} {record["mail_zipcode"]}")
        print()

        print(f"{fakeCCNumber()}")
        print(f"{fakeSSN()}")
        print(f"{fakeLicensePlate()}")
        print(f"{fakeProcedureCode()}")
        print()

        print(f"{fakeEmailAddress()}")
        print()

        print()

if __name__ == "__main__":
    main()
