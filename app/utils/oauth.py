# app/utils/oauth.py
import os
from flask import Flask, request, redirect, session, url_for
from authlib.integrations.flask_client import OAuth
import threading

# Configurações do OAuth do Google
GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID', 'YOUR_GOOGLE_CLIENT_ID')
GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET', 'YOUR_GOOGLE_CLIENT_SECRET')
SECRET_KEY = os.getenv('SECRET_KEY', 'your_secret_key')
API_BASE_URL = os.getenv('API_BASE_URL', 'http://127.0.0.1:5000')

app = Flask(__name__)
app.secret_key = SECRET_KEY
app.config['SESSION_COOKIE_NAME'] = 'google-login-session'

oauth = OAuth(app)
google = oauth.register(
    name='google',
    client_id=GOOGLE_CLIENT_ID,
    client_secret=GOOGLE_CLIENT_SECRET,
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_params=None,
    refresh_token_url=None,
    redirect_uri=f'{API_BASE_URL}/callback',
    client_kwargs={'scope': 'openid profile email'},
)

@app.route('/')
def home():
    return 'Welcome to the OAuth 2.0 Flask example!'

@app.route('/login')
def login():
    redirect_uri = url_for('authorize', _external=True)
    return google.authorize_redirect(redirect_uri)

@app.route('/authorize')
def authorize():
    token = google.authorize_access_token()
    resp = google.get('userinfo')
    user_info = resp.json()
    session['profile'] = user_info
    return redirect('/profile')

@app.route('/profile')
def profile():
    user_info = session['profile']
    return f"User: {user_info['name']}"

@app.route('/callback')
def callback():
    return redirect(url_for('authorize'))

def run_server():
    app.run(debug=False, port=5000, use_reloader=False)

def start_server():
    threading.Thread(target=run_server).start()
