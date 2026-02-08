#!/usr/bin/env python3
import sys
import os
from subfinder.passive import PassiveFinder
from subfinder.active import ActiveFinder
from subfinder.utils import deduplicate, save_results
from datetime import datetime

def main():
    if len(sys.argv) > 1:
        target = sys.argv[1]
    else:
        target = input("Enter target domain (e.g. google.com): ").strip()
    
    if not target:
        print("No domain provided.")
        sys.exit(1)
    
    print(f"Starting subdomain enumeration for {target}...")
    
    passive = PassiveFinder(target)
    active = ActiveFinder(target)
    
    print("Fetching passive subdomains...")
    passive_subs = passive.find_all()
    
    print("Running active enumeration...")
    active_subs = active.find_all()
    
    all_subs = passive_subs + active_subs
    unique_subs = deduplicate(all_subs)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"output/results_{timestamp}.txt"
    
    print(f"\nFound {len(unique_subs)} unique subdomains:")
    for sub in sorted(unique_subs):
        print(f"  {sub}")
    
    save_results(unique_subs, filename)
    print(f"\nResults saved to {filename}")

if __name__ == "__main__":
    os.makedirs("output", exist_ok=True)
    main()