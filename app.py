import os
import re
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, flash, session
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from werkzeug.security import generate_password_hash, check_password_hash  # Import password hashing

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Load the trained model
model_path = os.path.abspath('vitiligo_model.h5')
model = load_model(model_path)

# Configure upload folder
UPLOAD_FOLDER = 'static/uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the uploads directory exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Helper function to predict image
def predict_image(filepath):
    img = load_img(filepath, target_size=(150, 150))
    img_array = img_to_array(img) / 255.0
    img_array = img_array.reshape(1, 150, 150, 3)
    prediction = model.predict(img_array)
    return "Vitiligo" if prediction[0][0] > 0.5 else "Healthy Skin"


# Database setup logic
def init_db():
    connection = sqlite3.connect('users.db')
    cursor = connection.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        first_name TEXT NOT NULL,
                        last_name TEXT NOT NULL,
                        email TEXT NOT NULL UNIQUE,
                        password TEXT NOT NULL,
                        gender TEXT NOT NULL,
                        dob TEXT NOT NULL,
                        age INTEGER NOT NULL
                    )''')
    connection.commit()
    connection.close()


init_db()  # Initialize database


@app.route('/')
def index():
    return render_template('index.html')


# Signup
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Fetch data from form
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        gender = request.form['gender']
        dob = request.form['dob']
        age = int(request.form['age'])

        # Validate password
        if not re.match(r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,12}$', password):
            flash('Password must be 8-12 characters, include 1 uppercase, 1 lowercase, 1 number, and 1 special character.', 'error')
            return redirect(url_for('signup'))

        if password != confirm_password:
            flash('Passwords do not match.', 'error')
            return redirect(url_for('signup'))

        # Hash the password
        hashed_password = generate_password_hash(password)  # Password will be hashed

        # Insert into database (only hash for password, others remain plain text)
        connection = sqlite3.connect('users.db')
        cursor = connection.cursor()
        try:
            cursor.execute('''
                INSERT INTO users (first_name, last_name, email, password, gender, dob, age)
                VALUES (?, ?, ?, ?, ?, ?, ?)''',
                (first_name, last_name, email, hashed_password, gender, dob, age)
            )
            connection.commit()
            flash('Signup successful. Please login.', 'success')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('Email already exists.', 'error')
        finally:
            connection.close()

    return render_template('signup.html')


# Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Authenticate user
        connection = sqlite3.connect('users.db')
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM users WHERE email=?', (email,))
        user = cursor.fetchone()
        connection.close()

        # Check if user exists and validate the password
        if user and check_password_hash(user[4], password):  # Hash comparison on the password
            session['user'] = user[3]  # Store user's email in the session
            flash('Login successful.', 'success')
            return redirect(url_for('upload'))
        else:
            flash('Invalid credentials or account does not exist. Sign up first.', 'error')
            return redirect(url_for('login'))

    return render_template('login.html')


# Logout
@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('Logged out successfully.', 'success')
    return redirect(url_for('index'))




# Image Upload
@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if 'user' not in session:
        flash('Please log in first.', 'error')
        return redirect(url_for('login'))

    if request.method == 'POST':
        if 'image' not in request.files:
            flash('No image selected.', 'error')
            return redirect(url_for('upload'))
        file = request.files['image']
        if file.filename == '':
            flash('Please select a file.', 'error')
            return redirect(url_for('upload'))
        
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        prediction = predict_image(filepath)
        flash('Image uploaded and detection completed successfully.', 'success')
        return render_template('result.html', prediction=prediction, filepath=filepath)

    return render_template('upload.html')


if __name__ == '__main__':
    app.run(debug=True)
