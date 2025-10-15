#secret scanner

import argparse
import logging
import os
import re
from pathlib import Path

#patterns to search for
PATTERNS = [
    ("API", re.compile(r"[A-Za-z0-9_]{21}--[A-Za-z0-9_]{8}")),
    ("Twitter access token", re.compile(r"[1-9][0-9]+-[0-9a-zA-Z]{40}")),
    ("Facebook access token", re.compile(r"EAACEdEose0cBA[0-9A-Za-z]+")),
    ("Instagram OAuth2.0", re.compile(r"[0-9a-fA-F]{7}\.[0-9a-fA-F]{32}")),
    ("GitHub personal access token", re.compile(r"ghp_[a-zA-Z0-9]{36}")),
]

#build command line parser results
def parse_args():
    p = argparse.ArgumentParser(description="Scan a file or directory for common secret patterns.")
    p.add_argument("path", help="Path to file or directory to scan")
    p.add_argument("-v", "--verbose", action="store_true", help="Show debug output")
    return p.parse_args()

#open file and search for pattern
def scan_file(path: Path):
    try:
        with path.open("r", encoding="utf-8", errors="ignore") as fh:
            for lineno, line in enumerate(fh, start=1):
                for name, rx in PATTERNS:
                    for m in rx.finditer(line):
                        print(f"{path}:{lineno}: [{name}] {m.group(0)}")
    except Exception as e:
        logging.warning("Could not read %s: %s", path, e)

#determine if file or directory
def scan_path(target: Path):
    if target.is_file():
        scan_file(target)
    elif target.is_dir():
        for root, _, files in os.walk(target):
            for fname in files:
                scan_file(Path(root) / fname)
    else:
        logging.error("Not a file or directory: %s", target)

#main method
def main():
    args = parse_args()
    #set up logging
    logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO, format="%(levelname)s: %(message)s")
    target = Path(args.path)
    if not target.exists():
        logging.error("Path does not exist: %s", target)
        return
    logging.info("Starting scan on %s", target)
    scan_path(target)
    logging.info("Scan finished")

if __name__ == "__main__":
    main()