import requests

url = "https://jsonplaceholder.typicode.com/users"
response = requests.get(url)
print(response.status_code)
for user in response.json():
    print(f"{user['name']}")
    print(f"{user['username']}")
    print(f"{user['email']}")
    print(f"{user['company']['name']}")
    print(f"{user['phone']}")
    # get extension in phone number
    phone_extension = user['phone'].split(' ')[1] if ' ' in user['phone'] else ''
    print(f"Phone extension: {phone_extension}")