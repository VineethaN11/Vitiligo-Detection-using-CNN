# Vitiligo Detection using CNN

A web application that classifies a skin image as **Vitiligo** or **Healthy Skin** using a Convolutional Neural Network (CNN). Users sign up, log in, upload an image, and get a prediction.

> **Disclaimer:** This is an academic project and not a medical diagnostic tool. Consult a dermatologist for any medical concern.

## Features
- CNN-based binary image classification (Vitiligo vs. Healthy Skin)
- User signup and login with password hashing (Werkzeug)
- Password validation (8-12 characters, with uppercase, lowercase, number and special character)
- Image upload with instant prediction on a results page
- SQLite database for user accounts
- Session-based authentication; the upload page is available only to logged-in users

## Tech Stack
| Area | Tools |
|---|---|
| Model | Python, TensorFlow / Keras |
| Backend | Flask |
| Database | SQLite |
| Frontend | HTML, CSS (Jinja2 templates) |

## How It Works
1. The user uploads a skin image.
2. The image is resized to 150x150 and normalised to the 0-1 range.
3. The trained CNN outputs a probability. A value above 0.5 is classified as **Vitiligo**, otherwise **Healthy Skin**.
4. The result is shown on the results page.

## Project Structure
```
├── app.py                          # Flask app: routes, auth, prediction
├── vitiligo_model_training.ipynb   # Model training notebook
├── templates/                      # HTML pages (login, signup, upload, result)
├── static/                         # CSS and uploaded images
├── Healthy/, Vitiligo/, dataset/   # Image data
└── users.db                        # SQLite database (created automatically)
```

## Setup and Run
```bash
# 1. Clone the repo
git clone https://github.com/VineethaN11/Vitiligo-Detection-using-CNN.git
cd Vitiligo-Detection-using-CNN

# 2. Install dependencies
pip install flask tensorflow pillow werkzeug

# 3. Train the model
# Run vitiligo_model_training.ipynb and save the trained model
# as vitiligo_model.h5 in the project root.

# 4. Start the app
python app.py
```
Then open **http://127.0.0.1:5000** in your browser.

## Usage
1. Sign up with your details.
2. Log in.
3. Upload a skin image on the upload page.
4. View the prediction.

## Results
[Add your model's test accuracy here, for example: "Achieved XX% accuracy on the test set." Delete this section if you don't have a number.]

## Future Improvements
- Larger and more diverse dataset to improve generalisation
- Model evaluation with precision, recall and a confusion matrix
- Move the secret key to an environment variable
- Deploy the app online

## Author
**Vineetha N**
[GitHub](https://github.com/VineethaN11) | [LinkedIn](https://www.linkedin.com/in/vineetha-narayan-799111298/)
