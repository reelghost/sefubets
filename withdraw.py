import requests

headers = {
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOiI2ODA1MzZhNjg3MDM4ODAwMjk5ZWFhMzkiLCJpYXQiOjE3NDUzMjA4NzZ9.-6lqvQndkQzHmAdbrCtYjabU7kF8OuoVcdu1n51VCUo"
}
def user_data():
    url = "https://api.sofabets.com/api/auth/user"
    response = requests.get(url, headers=headers)
    data = response.json()
    print(data)
    balance = data.get('balance')
    return balance

def withdraw(balance):
    with_url = "https://api.sofabets.com/api/wallet/withdraw"
    with_payload = {"amount":balance}
    with_response = requests.post(with_url, json=with_payload, headers=headers)
    print(with_response.json())

if __name__ == "__main__":
    bal = user_data()
    if bal >= 100:
        withdraw(int(bal))
    print(int(bal))