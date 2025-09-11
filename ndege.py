import cloudscraper
import time
import csv
import random
import sys
import secrets

URL = "https://api.ganjibets.com/api/v1/user/create-account"
HEADERS = {
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOiI2OGMyYmMyZGFiYmY3N2ZiNWQ0NTYxZjIiLCJhY2NvdW50SWQiOiI2OGMyYmMyZGFiYmY3N2ZiNWQ0NTYxZjMiLCJ0ZW5hbnRJZCI6IjY4OWYyNDRlMDRkZTI0ZWRkN2Y1ZDdhZSIsInBob25lIjoiMDc5OTk5NjQ0MiIsImlhdCI6MTc1NzU5MjYyMiwiZXhwIjoxNzU4MTk3NDIyfQ.QRPc7Xx3LxhBE1XS3-0TjhOgpT_nv8QV3AWAdYDN27o"
}


def get_balance():
    bal_url = "https://api.ganjibets.com/api/v1/user/getUserBalance"
    resp = cloudscraper.create_scraper().get(bal_url, headers=HEADERS)
    data = resp.json()
    print(data)
    bal = data.get('balance')
    if bal >= 100:
        print(withdraw(bal))

def normalize_phone_number(phone: str) -> str:
    phone = phone.replace(' ', '')
    if phone.startswith('+254'):
        # Replace '+254' with '0'
        return '0' + phone[4:]
    return phone


def withdraw(amount):
    issue_url = "https://api.ganjibets.com/api/v1/wallet/createIssueKey"
    key_resp = cloudscraper.create_scraper().post(issue_url, headers=HEADERS)
    key = key_resp.json().get("withdrawTransactionKey")
    with_url = f"https://api.ganjibets.com/api/v1/wallet/withdraw/{key}"
    with_payload = {"amount":amount,"tenantId":"689f244e04de24edd7f5d7ae"}
    with_resp = cloudscraper.create_scraper().post(with_url, json=with_payload, headers=HEADERS)
    print(with_resp.json())


def register(phone_number: str):
    reg_url = f"https://api.ganjibets.com/api/v1/user/create-account"
    reg_payload = {
        "phone":phone_number,
        "password":phone_number,
        # "tenantId": secrets.token_hex(24),
        "tenantId": "689f244e04de24edd7f5d7ae",
        "referralCode":"KUM0OFIH"
    }
    scraper = cloudscraper.create_scraper()
    # Step 2: Using the same session, send a POST request to reg_url with the payload
    response_post = scraper.post(reg_url, json=reg_payload)
    response_post_json = response_post.json()
    print(response_post_json)
    message = response_post.json().get('message')
    print(f"[REG] {message}")

def read_phone_numbers_from_csv(csv_file: str):
    phone_numbers = []
    with open(csv_file, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # phone = row.get('Phone 1 - Value') # for google sheets csv
            phone = row.get('PhoneNumber') # for csv
            if phone:
                # Optionally, clean/strip the phone number
                norm_phone = normalize_phone_number(phone.strip())
                phone_numbers.append(norm_phone)
    return phone_numbers

def generate_random_phone_number():
    # Generates a random Kenyan phone number starting with '072'
    import random
    suffix = ''.join(str(random.randint(0, 9)) for _ in range(7))
    p_number = "079" + suffix
    return p_number

if __name__ == "__main__":
    p_numbers = read_phone_numbers_from_csv('contacts.csv')
    for number in p_numbers:
        print(f"Processing {number}")
        register(number)
        get_balance()
  