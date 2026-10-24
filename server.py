from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse
import sqlite3
import os

Host = "localhost"
Port = 8000

dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(dir, "users.db")

def Data_base():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)")
    cursor.execute("SELECT * FROM users WHERE username='admin'")
    if not cursor.fetchone():
        cursor.execute("INSERT INTO users (username, password) VALUES ('admin', 'admin_password')")
        conn.commit()
    conn.close()

class Server(BaseHTTPRequestHandler):

    def do_GET(self):

        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()

        html = """
        <!DOCTYPE HTML>
        <html>
        <head>
        <meta charset="utf-8">
        <title>Сайт на Python</title>
        </head>
        <body>
            <h2>Введите логин и пароль:</h2>
            <form method="POST" action="/">
                <p>Логин: <input type="text" name="login" required></p>
                <p>Пароль: <input type="text" name="password" required></p>
                <input type="submit" value="Войти">
            </form>
        </body>
        </html>
        """

        self.wfile.write(html.encode("utf-8"))

    def do_POST(self):

        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')

        parsed_data = urllib.parse.parse_qs(post_data)
        user_login = parsed_data.get('login', [''])[0]
        user_password = parsed_data.get('password', [''])[0]

        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        sql_query = f"SELECT * FROM users WHERE username = '{user_login}' AND password = '{user_password}'"

        try:
            cursor.execute(sql_query)
            account = cursor.fetchone()
        except Exception:
            account = None

        conn.close()

        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()

        if account:
            result = f"<h1> Успешно! Вы вошли как админ {user_login}! </h1>"
            print("Вы успешно вошли как администратор")
        else:
            result = f"<h1> Неверный логин или пароль. Вход запрещен {user_login}! </h1>"
            print("Вход запрещен!")
        html_response = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Результат обработки</title>
        </head>
        <body>
                {result}   
            <strong><a href="/">← Вернуться назад к форме</a></strong>
        </body>
        </html>
        """
        self.wfile.write(html_response.encode("utf-8"))

def run():
    Data_base()
    server_address = (Host, Port)
    httpd = HTTPServer(server_address, Server)
    print(f"Сервер запущен на http://{Host}:{Port}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Сервер остановлен")
        httpd.server_close()
if __name__ == "__main__":
    run()