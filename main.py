import cloudscraper
import time
import csv
import random

def normalize_phone_number(phone: str) -> str:
    phone = phone.replace(' ', '')
    if phone.startswith('+254'):
        # Replace '+254' with '0'
        return '0' + phone[4:]
    return phone

def reset_password(phone_number: str):
    reset_pswd_url = "https://api.sofabets.com/api/auth/password_reset"
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
    password = "50bob"
    ref_url = f"https://www.sofabets.com?ref=680536a687038800299eaa39"
    reg_url = "https://api.sofabets.com/api/auth/register"
    reg_payload = {
        "phone": phone_number,
        "password": password,
        "confirmPassword": password,
        # "fingerprint": "1c81e9d6b688a9c5115306b74c6067ea",
        "referrer": "680536a687038800299eaa39"
    }
    scraper = cloudscraper.create_scraper()
    # Step 1: Go to ref_url with a GET request
    scraper.get(ref_url)
    # Step 2: Using the same session, send a POST request to reg_url with the payload
    response_post = scraper.post(reg_url, json=reg_payload)
    response_post_json = response_post.json()
    print(response_post_json)
    message = response_post.json().get('message')
    print(f"[REG] {message}")
    if message:
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

if __name__ == "__main__":
    p_numbers = read_phone_numbers_from_csv('contacts.csv')
    for number in p_numbers:
        print(f"Processing {number}")
        register(number)
    # a while loop to generate random number and register them
    # while True:
    #     phone_number = generate_random_phone_number()
    #     print(f"Processing {phone_number}")
    #     register(phone_number)
    #     time.sleep(2)