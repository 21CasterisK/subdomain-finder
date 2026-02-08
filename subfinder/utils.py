import re
from pathlib import Path
from tqdm import tqdm

def deduplicate(subdomains):
    return list(set([s for s in subdomains if s]))

def save_results(subdomains, filename):
    Path(filename).write_text("\n".join(sorted(subdomains)) + "\n")

def load_wordlist(path):
    if not Path(path).exists():
        return []
    return [w.strip() for w in Path(path).read_text().strip().split("\n") if w.strip()]

def is_valid_subdomain(sub):
    pattern = re.compile(
        r'^([a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}$'
    )
    return bool(pattern.match(sub))