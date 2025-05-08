
import webbrowser
import requests
from flask import Flask, request
from requests_oauthlib import OAuth2Session
import os
from dotenv import load_dotenv

# Enable HTTPS enforcement if deployed on Render
load_dotenv()

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "0"

# OAuth 2.0 Credentials from Environment Variables
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI", "https://your-app.onrender.com/callback")
AUTH_URL = "https://accounts.google.com/o/oauth2/auth"
TOKEN_URL = "https://oauth2.googleapis.com/token"
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

app = Flask(__name__)
oauth = OAuth2Session(CLIENT_ID, redirect_uri=REDIRECT_URI, scope=SCOPES)

@app.route("/")
def home():
    """ Redirect users to Google OAuth """
    auth_url, _ = oauth.authorization_url(AUTH_URL)
    return f'<a href="{auth_url}">Login with Google</a>'

@app.route("/callback")
def callback():
    """ Handle OAuth callback and fetch emails """
    token = oauth.fetch_token(TOKEN_URL, client_secret=CLIENT_SECRET, authorization_response=request.url)
    emails = fetch_emails(token)
    return {"Access Token": token['access_token'], "Emails": emails}

def fetch_emails(token):
    """ Retrieve Gmail emails using token """
    gmail_api_url = "https://gmail.googleapis.com/gmail/v1/users/me/messages"
    headers = {"Authorization": f"Bearer {token['access_token']}"}
    response = requests.get(gmail_api_url, headers=headers)
    return response.json()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
