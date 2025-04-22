from flask import Flask, redirect, url_for, session
from authlib.integrations.flask_client import OAuth
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

oauth = OAuth(app)
github = oauth.register(
    name='github',
    client_id='Ov23liolrz8yPeNv8exe',
    client_secret='ddec247a40c03f7997880c134992c0023b788921',
    access_token_url='https://github.com/login/oauth/access_token',
    access_token_params=None,
    authorize_url='https://github.com/login/oauth/authorize',
    authorize_params=None,
    api_base_url='https://api.github.com/',
    client_kwargs={'scope': 'user:email'},
)

@app.route('/')
def index():
    user = session.get('user')
    if user:
        return f"Hello, {user['login']}! <br><a href='/logout'>Logout</a>"
    return '<a href="/login">Login with GitHub</a>'

@app.route('/login')
def login():
    redirect_uri = url_for('callback', _external=True)
    return github.authorize_redirect(redirect_uri)

@app.route('/callback')
def callback():
    token = github.authorize_access_token()
    resp = github.get('user')
    user_info = resp.json()
    session['user'] = user_info
    return redirect('/')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)  # Allow LAN access

