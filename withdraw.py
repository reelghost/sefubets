import requests

URL = "https://devapi.safibets.com/api"

headers = {
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOiI2ODE1MmFkZWIxNmJjNDc1OTMwN2Y1NjMiLCJpYXQiOjE3NDYyMTgyMzd9.epVx_LRBNa72BEhjWmz7tDgFyDE2Pc4OfpY8Mf19Mjs"
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