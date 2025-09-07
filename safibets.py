import cloudscraper
import time
import csv
import random
import secrets
import sys

URL = "https://back.safibets.com/api"
HEADERS = {
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOjEzNzcwOCwicGhvbmUiOiIwNzk5OTk2NDQyIiwiaWF0IjoxNzU1MTkxOTI2fQ.-j412Tw3zlGyaiNmqWMClZnfDk9IGa2hNN3ZgyFfuVU"
}

def get_number_of_refs():
    resp = requests.get(f"{URL}/auth/user", headers=HEADERS)
    data = resp.json()
    return data.get('total_referrals')

def normalize_phone_number(phone: str) -> str:
    phone = phone.replace(' ', '')
    if phone.startswith('+254'):
        # Replace '+254' with '0'
        return '0' + phone[4:]
    return phone

def reset_password(phone_number: str):
    reset_pswd_url = f"{URL}/auth/password_reset"
    reset_payload = {"phoneNumber": phone_number}
    # Wait 2 seconds
    time.sleep(2)
    # Send a POST request for reset password with the used number
    scraper = cloudscraper.create_scraper()
    response_reset = scraper.post(reset_pswd_url, json=reset_payload)
    message = response_reset.json().get('message')
    print(f"[RESET] {message}")

def register(phone_number: str):
    # password = phone_number[-4:]
    password = "win500"
    reg_url = f"{URL}/auth/register"
    reg_payload = {
        "phone":phone_number,
        "password":password,
        "confirmPassword":password,
        "fingerprint": secrets.token_hex(16),
        "referrer":"137708"
    }
    scraper = cloudscraper.create_scraper()
    # Step 2: Using the same session, send a POST request to reg_url with the payload
    response_post = scraper.post(reg_url, json=reg_payload)
    response_post_json = response_post.json()
    print(response_post_json)
    message = response_post.json().get('message')
    print(f"[REG] {message}")
    if message and "registration successful" in message.lower() or "already registered" in message.lower():
        reset_password(phone_number)

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
    p_number = "072" + suffix
    return p_number

def main():
    if len(sys.argv) > 1:
        number = sys.argv[1]
    else:
        print("Please provide a phone number as the first argument")
        sys.exit(1)
    register(number)
if __name__ == "__main__":
    main()

if __name__ == "__main__":
    main()
    # p_numbers = read_phone_numbers_from_csv('contacts.csv')
    # for number in p_numbers:
    #     print(f"Processing {number}")
    #     register(number)
    print("Number of referrals: ", get_number_of_refs())
    
    # a while loop to generate random number and register them
    # while True:
    #     phone_number = generate_random_phone_number()
    #     print(f"Processing {phone_number}")
    #     register(phone_number)
    #     time.sleep(1)
