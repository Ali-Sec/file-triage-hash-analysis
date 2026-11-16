"""
File Triage & Hash Analysis Tool
COMP H2702 - Scripting for Cybersecurity

Checks every file in a folder, calculates its SHA-256 hash,
compares it with a list of known hashes, finds duplicate files,
and saves a CSV report.

Usage:  python triage.py [folder]
"""

import os
import sys
import csv
import hashlib
from datetime import datetime


def get_sha256(path):
    """Return the SHA-256 hash of a file, or None if it can't be read."""
    try:
        with open(path, "rb") as f:
            data = f.read()
        return hashlib.sha256(data).hexdigest()
    except OSError as error:
        print("   ERROR: could not read", path, "-", error)
        return None


def load_reference(csv_path):
    """Load known hashes from the CSV into a dictionary {hash: label}."""
    known = {}
    try:
        with open(csv_path, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                file_hash = (row.get("sha256") or "").strip().lower()
                label = (row.get("label") or "").strip()
                if len(file_hash) != 64:
                    print("WARNING: skipping bad line in", csv_path, "->", row)
                    continue
                known[file_hash] = label
    except FileNotFoundError:
        print("WARNING:", csv_path, "not found. All files will be UNKNOWN.")
    return known


def print_duplicates(hash_groups):                           
    """Print groups of files that have the same hash."""
    print()
    print("Duplicate check:")
    found = False
    for file_hash, names in hash_groups.items():
        if len(names) > 1:
            print("   Same content:", ", ".join(names))
            found = True
    if not found:
        print("   No duplicates found")


def save_report(results, report_path):
    """Save the results list to a CSV file."""
    columns = ["filename", "extension", "size_bytes",
               "modified", "sha256", "status", "label"]
    try:
        with open(report_path, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=columns)
            writer.writeheader()
            for row in results:
                writer.writerow(row)
        print("Report saved to", report_path)
    except PermissionError:
        print("ERROR: could not save", report_path,
              "- is it open in Excel? Close it and run again.")


def main():                                                  
    if len(sys.argv) > 1:                                    
        folder = sys.argv[1]
    else:
        folder = "samples"

    print("Checking folder:", folder)
    print()

    known_hashes = load_reference("hashes_reference.csv")
    hash_groups = {}
    results = []

    try:
        filenames = os.listdir(folder)
    except FileNotFoundError:
        print("ERROR: the folder", folder, "does not exist.")
        return

    for filename in filenames:
        path = os.path.join(folder, filename)
        if not os.path.isfile(path):
            continue

        extension = os.path.splitext(filename)[1]
        size = os.path.getsize(path)
        modified = datetime.fromtimestamp(os.path.getmtime(path))
        modified = modified.strftime("%Y-%m-%d %H:%M")
        file_hash = get_sha256(path)

        if file_hash is None:
            status = "ERROR"
            label = "could not read file"
        elif file_hash in known_hashes:
            status = "KNOWN"
            label = known_hashes[file_hash]
        else:
            status = "UNKNOWN"
            label = ""

        print(filename, extension, size, "bytes", modified)
        print("   SHA-256:", file_hash)
        print("   Status:", status, label)

        results.append({
            "filename": filename,
            "extension": extension,
            "size_bytes": size,
            "modified": modified,
            "sha256": file_hash,
            "status": status,
            "label": label,
        })

        if file_hash is not None:
            if file_hash not in hash_groups:
                hash_groups[file_hash] = []
            hash_groups[file_hash].append(filename)

    print_duplicates(hash_groups)
    print()
    save_report(results, "triage_report.csv")


if __name__ == "__main__":                                   
    main()