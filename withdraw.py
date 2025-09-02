import requests

URL = "https://back.sofabets.com/api"

headers = {
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOjY4MTgwLCJwaG9uZSI6IjA3OTk5OTY0NDIiLCJpYXQiOjE3NTY3OTU2MTF9.sPcJxWOwu0-fgDp7U0v5dpVhydA6aLyxKgTP-Kp-yM0"
}
def user_data():
    url = f"{URL}/auth/user"
    response = requests.get(url, headers=headers)
    data = response.json()
    print(data)
    balance = data.get('balance')
    return balance

def withdraw(balance):
    with_url = f"{URL}/wallet/withdraw"
    with_payload = {"amount":balance}
    with_response = requests.post(with_url, json=with_payload, headers=headers)
    print(with_response.json())

if __name__ == "__main__":
    bal = user_data()
    if bal >= 100:
        withdraw(int(bal))
    print(int(bal))