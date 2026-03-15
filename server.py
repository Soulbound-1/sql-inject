from flask import Flask, request, render_template_string, g
import sqlite3

app = Flask(__name__)
DATABASE = 'users.db'

# Setup local database
def init_db():
    with sqlite3.connect(DATABASE) as conn:
        conn.execute('CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT, role TEXT)')
        conn.execute("INSERT OR IGNORE INTO users VALUES ('admin', 'p@ssword123', 'superuser')")
        conn.execute("INSERT OR IGNORE INTO users VALUES ('omkar', 'secure_dev_2026', 'developer')")
        conn.commit()

init_db()

@app.route('/')
def home():
    # VULNERABILITY: Reflected XSS
    # The 'name' parameter is rendered directly without sanitization.
    name = request.args.get('name', 'Guest')
    template = f"<h1>Welcome, {name}!</h1><p>Try logging in at /login</p>"
    return render_template_string(template)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form.get('username')
        pw = request.form.get('password')
        
        # VULNERABILITY: SQL Injection (CWE-89)
        # Using string formatting instead of parameterized queries.
        query = f"SELECT role FROM users WHERE username = '{user}' AND password = '{pw}'"
        
        try:
            with sqlite3.connect(DATABASE) as conn:
                cursor = conn.cursor()
                cursor.execute(query)
                result = cursor.fetchone()
                
                if result:
                    return f"Login successful! Your role is: {result[0]}"
                return "Invalid credentials.", 401
        except Exception as e:
            return f"Database Error: {str(e)}", 500

    return '''
        <form method="post">
            Username: <input type="text" name="username"><br>
            Password: <input type="password" name="password"><br>
            <input type="submit" value="Login">
        </form>
    '''

if __name__ == '__main__':
    app.run(port=5000)
