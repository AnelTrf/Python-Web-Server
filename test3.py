import http.server
import socketserver
import sqlite3
import hashlib
from urllib.parse import urlparse, parse_qs
from jinja2 import Template
import os
import uuid
import webbrowser

conn = sqlite3.connect('mydatabase.db')

# Create a cursor object
cursor = conn.cursor()
cursor.execute('SELECT * FROM users')

# Retrieve the data
data = cursor.fetchall()

# Create a table in the database
# cursor.execute('''CREATE TABLE IF NOT EXISTS users
#                  (id INTEGER PRIMARY KEY,
#                  username TEXT,
#                  password text)''')
#
# cursor.execute(''' CREATE TABLE IF NOT EXISTS contras
#              (id text PRIMARY KEY,
#              Name text,
#              bin text,
#              checking_account text,
#              address text,
#              phone text,
#              email text,
#              director text,
#              accountant text
#              )''')

#
# cursor.execute(''' CREATE TABLE IF NOT EXISTS lines
#              (id text PRIMARY KEY,
#              name text,
#              pin text,
#              type text,
#              keys text,
#              control text
#              )''')
#
# cursor.execute('''CREATE TABLE IF NOT EXISTS ctos
#                  (id text PRIMARY KEY,
#                  name text,
#                  choice text,
#                  address text,
#                  phone text,
#                  email text,
#                  head text
#                  )''')

cursor.execute('DROP TABLE IF EXISTS lines')

# Insert the hashed password into the database
username1, password1 = "AnelTrf", hashlib.sha256("12345678".encode()).hexdigest()
# cursor.execute("INSERT INTO users (id, username, password) VALUES (?, ?, ?)", (2, username1, password1))

name, address = "TOO", "Almaty"
# cursor.execute("INSERT INTO contras (name, address) VALUES(?,?)", (name, address))

# # Commit the changes to the database
# conn.commit()

# # Close the database connection
# conn.close()

# def delete_record(name):
#     # conn = sqlite3.connect('mydatabase.db')
#     # c = conn.cursor()
#     cursor.execute('DELETE FROM contras WHERE name = ?', (name,))
#     # conn.commit()
#     # conn.close()

class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):

    def __init__(self, *args, **kwargs):
        # self.template = Template.render
        self.conn = None
        super().__init__(*args, **kwargs)

    def setup(self):
        super().setup()
        # Create a connection to the database
        self.conn = sqlite3.connect('mydatabase.db')

    def teardown(self):
        if self.conn:
            # Close the database connection
            self.conn.close()
        super().teardown()


    def do_POST(self):
        if self.path == '/new':
            # Get the form data from the request
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            form_data = parse_qs(post_data)

            id = str(uuid.uuid4())
            name = form_data['Name'][0]
            bin = form_data['bin'][0]
            checking_account = form_data['checking_account'][0]
            address = form_data['address'][0]
            phone = form_data['phone'][0]
            email = form_data['email'][0]
            director = form_data['director'][0]
            accountant = form_data['accountant'][0]
            button = form_data['button'][0]
            # Insert the data into the contras table
            if button == 'Сохранить':
                # Insert the data into the ctos table
                cursor.execute(
                    "INSERT INTO contras (id, Name, bin, checking_account, address, phone, email, director, accountant) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (id, name, bin, checking_account, address, phone, email,director,accountant))
            elif button == 'Удалить':
                # Delete the data from the ctos table
                cursor.execute(
                    "DELETE FROM contras WHERE Name = ? AND bin = ? AND checking_account = ? AND address = ? AND phone = ? AND email = ? AND director = ? AND accountant = ?",
                    (name, bin, checking_account, address, phone, email, director, accountant))

            # Commit the changes to the database
            conn.commit()

            # Redirect to the contras page
            self.send_response(302)
            self.send_header('Location', '/contra')
            self.end_headers()

        elif self.path == '/cto':
            # Get the form data from the request
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            form_data = parse_qs(post_data)

            id = str(uuid.uuid4())
            Name = form_data['name'][0]
            choice = form_data['choice'][0]
            Address = form_data['address'][0]
            Phone = form_data['phone'][0]
            Email = form_data['email'][0]
            head = form_data['head'][0]
            button = form_data['button'][0]
            if button == 'Сохранить':
                # Insert the data into the ctos table
                cursor.execute(
                    "INSERT INTO ctos (id, name, choice, address, phone, email, head) VALUES (?, ?, ?, ?, ?, ?, ?)",
                    (id, Name, choice, Address, Phone, Email, head))
            elif button == 'Удалить':
                # Delete the data from the ctos table
                cursor.execute(
                    "DELETE FROM ctos WHERE name = ? AND choice = ? AND address = ? AND phone = ? AND email = ? AND head = ?",
                    (Name, choice, Address, Phone, Email, head))
            # Commit the changes to the database
            conn.commit()

            # Redirect to the contras page
            self.send_response(302)
            self.send_header('Location', '/contra')
            self.end_headers()

        elif self.path == '/line':
            # Get the form data from the request
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            form_data = parse_qs(post_data)

            name = form_data['name'][0]
            pin = form_data['pin'][0]
            type = form_data['type'][0]
            # choice = request.form_data_parser_class['choice'][0]
            keys = form_data['keys'][0]
            control = form_data['colors'][0]
            button = form_data['button'][0]
            # Insert the data into the ctos table

            if button == 'Сохранить':
                # Insert the data into the ctos table
                cursor.execute(
                    "INSERT INTO lines (name, pin, type, keys, control) VALUES (?, ?, ?, ?, ?)",
                    (name, pin, type, keys, control))
            elif button == 'Удалить':
                # Delete the data from the ctos table
                cursor.execute(
                    "DELETE FROM lines WHERE name = ? AND pin = ? AND type = ? AND keys = ? AND control = ?",
                    (name, pin, type, keys, control))

            # cursor.execute(
            #     "INSERT INTO lines (name, pin, type, keys, control) VALUES (?, ?, ?, ?, ?)",
            #     (name, pin, type, keys, control))

            # Commit the changes to the database
            conn.commit()

            # Redirect to the contras page
            self.send_response(302)
            self.send_header('Location', '/contra')
            self.end_headers()

        elif self.path == '/':
            # Get the form data from the request
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            form_data = parse_qs(post_data)
            username = form_data['username'][0]
            cursor.execute("SELECT * FROM users WHERE username=?", (username,))
            user = cursor.fetchone()
            if user:
                # User is in the database
                self.send_response(302)
                self.send_header('Location', '/main')
                self.end_headers()

            else:
                # User is not in the database
                self.send_response(200)
                self.send_header('Location', '/')
                self.end_headers()

    def do_GET(self):
        parsed_url = urlparse(self.path)

        if self.path == '/':
            self.path = 'index.html'

        elif self.path == '/contra':
            # Retrieve data from the contras table
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM contras")
            rows = cursor.fetchall()
            cursor.execute("SELECT * FROM ctos")
            data = cursor.fetchall()

            # Generate an HTML table using a Jinja2 template
            with open('contras.html', encoding="utf8") as f:
                template = Template(f.read())
                html = template.render(rows=rows, data=data)
            # Write the generated HTML to the response and send it back to the client
            self.send_response(200)
            self.end_headers()
            self.wfile.write(html.encode())
            self.path = 'contr.html'

        elif parsed_url.path.startswith('/contra/'):
            # Retrieve the UUID from the URL path
            uuid_str = parsed_url.path.split('/')[-1]
            cursor = self.conn.cursor()
            # Query the database for the record with the matching UUID
            cursor.execute('SELECT Name, address FROM contras WHERE id = ?', (uuid_str,))
            record = cursor.fetchone()
            if record is not None:
                with open('new1.html', encoding="utf8") as f:
                    template = Template(f.read())
                    rendered_template = template.render(record=dict(
                        zip(['Name', 'address'], record)))
                    # rendered_template = template.render(record=record)
                # Send the rendered web page as the response
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(rendered_template.encode('utf-8'))
                self.path = 'contr.html'
        elif self.path == '/new':
            self.path = 'newcontra.html'
        elif self.path == '/cto':
            self.path = 'cto.html'
        elif self.path == '/line':
            self.path = 'line.html'
        elif self.path == '/module':
            self.path = 'module.html'
        elif self.path == '/revise':
            self.path = 'revise.html'
        elif self.path == '/revise-form':
            self.path = 'reviseForm.html'
        elif self.path == '/rev-form':
            self.path = 'revForm.html'
        elif self.path == '/revise-contra':
            # Retrieve data from the contras table
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM contras")
            rows = cursor.fetchall()

            # Generate an HTML table using a Jinja2 template
            with open('revisecontra.html', encoding="utf8") as f:
                template = Template(f.read())
                html = template.render(rows=rows)

            # Write the generated HTML to the response and send it back to the client
            self.send_response(200)
            self.end_headers()
            self.wfile.write(html.encode())
            self.path = 'rev.html'

        elif self.path == '/main':
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM contras")
            rows = cursor.fetchall()
            cursor.execute("SELECT * FROM ctos")
            data = cursor.fetchall()

            # Generate an HTML table using a Jinja2 template
            with open('contras.html', encoding="utf8") as f:
                template = Template(f.read())
                html = template.render(rows=rows, data=data)

            # Write the generated HTML to the response and send it back to the client
            self.send_response(200)
            self.end_headers()
            self.wfile.write(html.encode())
            self.path = 'contr.html'
        elif self.path == '/users':
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM users")
            rows = cursor.fetchall()
            with open('users.html', encoding="utf8") as f:
                template = Template(f.read())
                html = template.render(rows=rows)
                # Write the generated HTML to the response and send it back to the client
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(html.encode())
            self.path = 'use.html'

        return http.server.SimpleHTTPRequestHandler.do_GET(self)


file_path = "new1.html"
if os.path.exists(file_path):
    print("The file exists")
else:
    print("The file does not exist")

#Create an object of the above class
handler_object = MyHttpRequestHandler

PORT = 8080
my_server = socketserver.TCPServer(("", PORT), handler_object)

# Start the server
my_server.serve_forever()