from flask import Flask, render_template, request, redirect, session
import sqlite3
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "potato"

UPLOAD_FOLDER = os.path.join('static', 'uploaded_videos')
ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def get_user_from_db(username, password):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    user = cursor.fetchone()
    conn.close()
    return user

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form["username"]
        password = request.form["password"]

        user = get_user_from_db(username, password)

        if user:
            session['user'] = user[1]
            session['role'] = user[3]
            return redirect("/dashboard")
        else:
            print("Invalid Password or Username")
    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    if session['user']:
        return render_template("dashboard.html", user=session.get('user'))
    else:
        return redirect("/login")

@app.route('/videos')
def view_videos():
    if 'user' in session:
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT title, filename FROM videos")
        videos = cursor.fetchall()
        conn.close()

        return render_template('videos.html', videos=videos)
    else:
        return redirect('/login')

@app.route('/upload', methods=['GET', 'POST'])
def upload_video():
    if 'user' in session and session['role'] == 'admin':
        if request.method == 'POST':
            if 'file' not in request.files:
                return "No file part"
            file = request.files['file']
            if file.filename == '':
                return "No selected file"
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                
                # Save video info to the database
                title = request.form['title']
                conn = sqlite3.connect('database.db')
                cursor = conn.cursor()
                cursor.execute("INSERT INTO videos (title, filename) VALUES (?, ?)", (title, filename))
                conn.commit()
                conn.close()

                return redirect('/videos')
        return render_template('upload.html')
    else:
        return redirect('/dashboard')

        

app.run(debug=True)