import socket
import dns.resolver
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from subfinder.utils import load_wordlist, is_valid_subdomain
from tqdm import tqdm
import time

class ActiveFinder:
    def __init__(self, target, max_threads=100):
        self.target = target
        self.results = set()
        self.max_threads = max_threads
        self.wordlists = {
            'subdomains': 'wordlists/subdomains.txt',
            'permutations': 'wordlists/permutations.txt'
        }
    
    def resolve_dns(self, subdomain):
        try:
            socket.gethostbyname(subdomain)
            return True
        except:
            try:
                dns.resolver.resolve(subdomain, 'A', lifetime=2)
                return True
            except:
                return False
    
    def bruteforce(self, wordlist_path):
        words = load_wordlist(wordlist_path)
        print(f"Testing {len(words)} subdomains...")
        
        with ThreadPoolExecutor(max_workers=self.max_threads) as executor:
            futures = {
                executor.submit(self.resolve_dns, f"{word}.{self.target}"): word 
                for word in words
            }
            
            with tqdm(total=len(words), desc="Bruteforce") as pbar:
                for future in as_completed(futures):
                    if future.result():
                        sub = f"{futures[future]}.{self.target}"
                        self.results.add(sub)
                    pbar.update(1)
                    time.sleep(0.001)
    
    def permutations(self):
        perms = load_wordlist(self.wordlists['permutations'])
        print(f"Testing {len(perms)} permutations...")
        
        with ThreadPoolExecutor(max_workers=self.max_threads//2) as executor:
            futures = {
                executor.submit(self.resolve_dns, f"{perm}.{self.target}"): perm 
                for perm in perms
            }
            
            with tqdm(total=len(perms), desc="Permutations") as pbar:
                for future in as_completed(futures):
                    if future.result():
                        sub = f"{futures[future]}.{self.target}"
                        self.results.add(sub)
                    pbar.update(1)
    
    def find_all(self):
        self.bruteforce(self.wordlists['subdomains'])
        self.permutations()
        return list(self.results)