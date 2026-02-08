import requests
import dns.resolver
from urllib.parse import urlparse
from subfinder.utils import load_wordlist, is_valid_subdomain

class PassiveFinder:
    def __init__(self, target):
        self.target = target
        self.results = set()
    
    def crt_sh(self):
        url = f"https://crt.sh/?q=%25.{self.target}&output=json"
        try:
            resp = requests.get(url, timeout=10)
            if resp.status_code == 200:
                data = resp.json()
                for entry in data:
                    name = entry.get('name_value', '')
                    subs = name.split('\n')
                    for sub in subs:
                        sub = sub.strip().lower()
                        if self.target in sub and is_valid_subdomain(sub):
                            self.results.add(sub)
        except:
            pass
    
    def dns_records(self):
        records = ['A', 'AAAA', 'MX', 'NS', 'TXT', 'CNAME']
        for rtype in records:
            try:
                answers = dns.resolver.resolve(self.target, rtype)
                for rdata in answers:
                    if hasattr(rdata, 'exchange'):
                        self.results.add(rdata.exchange.to_text().rstrip('.'))
                    elif hasattr(rdata, 'target'):
                        self.results.add(rdata.target.to_text().rstrip('.'))
            except:
                pass
    
    def find_all(self):
        self.crt_sh()
        self.dns_records()
        return list(self.results)