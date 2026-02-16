from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import sqlite3
import os

app = Flask(__name__)

# Base paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")
DB_PATH = os.path.join(BASE_DIR, "users.db")

app.config["UPLOAD_FOLDER"] = UPLOAD_DIR

# Ensure uploads folder exists
os.makedirs(UPLOAD_DIR, exist_ok=True)


# ------------------------
# Database Initialization
# ------------------------
def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            password TEXT,
            firstname TEXT,
            lastname TEXT,
            email TEXT,
            address TEXT
        )
    """)
    conn.commit()
    conn.close()


init_db()


def get_user(username):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=?", (username,))
    user = c.fetchone()
    conn.close()
    return user


# ------------------------
# Routes
# ------------------------

@app.route("/")
def index():
    return render_template("register.html")


@app.route("/register", methods=["POST"])
def register():
    data = (
        request.form["username"],
        request.form["password"],
        request.form["firstname"],
        request.form["lastname"],
        request.form["email"],
        request.form["address"],
    )

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "INSERT INTO users (username, password, firstname, lastname, email, address) VALUES (?, ?, ?, ?, ?, ?)",
        data,
    )
    conn.commit()
    conn.close()

    return redirect(url_for("profile", username=data[0]))


@app.route("/profile/<username>")
def profile(username):
    user = get_user(username)
    return render_template("profile.html", user=user)


@app.route("/login")
def login_page():
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def login_submit():
    username = request.form["username"]
    password = request.form["password"]

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "SELECT * FROM users WHERE username=? AND password=?",
        (username, password),
    )
    user = c.fetchone()
    conn.close()

    if user:
        return redirect(url_for("profile", username=username))

    return render_template("login.html", error="Invalid username or password")

from werkzeug.utils import secure_filename

@app.route('/upload/<username>', methods=['POST'])
def upload_file(username):
    if 'file' not in request.files:
        return render_template('profile.html', user=get_user(username), error="No file part")

    file = request.files['file']

    if file.filename == '':
        return render_template('profile.html', user=get_user(username), error="No file selected")

    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    # Count words
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
        word_count = len(content.split())

    return render_template(
        'profile.html',
        user=get_user(username),
        word_count=word_count,
        uploaded_filename=filename   # ✅ IMPORTANT
    )

@app.route("/download/<filename>")
def download_file(filename):
    return send_from_directory(
        app.config["UPLOAD_FOLDER"],
        filename,
        as_attachment=True
    )


if __name__ == "__main__":
    app.run(debug=True)