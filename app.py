from flask import Flask, request, redirect, url_for, session
from requests_oauthlib import OAuth2Session
import os
from dotenv import load_dotenv
import requests
import json

# Enable HTTPS enforcement
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "0"

# OAuth 2.0 Credentials from Environment Variables
load_dotenv()
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI", "https://your-app.onrender.com/callback")
AUTH_URL = "https://accounts.google.com/o/oauth2/auth"
TOKEN_URL = "https://oauth2.googleapis.com/token"
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

# Adjustment for Windows Dev
if os.name == "nt":
    REDIRECT_URI = "http://127.0.0.1:5000/callback"
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
    

app = Flask(__name__)
oauth = OAuth2Session(CLIENT_ID, redirect_uri=REDIRECT_URI, scope=SCOPES)

@app.route("/")
def home():
    """ Redirect users to Google OAuth """
    auth_url, _ = oauth.authorization_url(AUTH_URL)
    return f'<a href="{auth_url}">Login with Google</a>'

@app.route("/success")
def success(labels=None):
    data = request.args.get("data", "[]")
    labels = json.loads(data)
    return f"<a>Success! Check out the terminal</a> </br> <a> List of labels = {listOfLabels(labels)}</a>"

@app.route("/callback")
def callback():
    """ Handle OAuth callback and fetch emails """
    token = oauth.fetch_token(TOKEN_URL, client_secret=CLIENT_SECRET, authorization_response=request.url)
    rawLabels = fetch_labels(token)
    labels = refinedLabels(rawLabels)

    return redirect(url_for("success", data=json.dumps(labels)))

def refinedLabels(rawLabels):
    for label in rawLabels:
        label["displayName"] = label["name"].lower().replace("_"," ").title()
    return rawLabels

def listOfLabels(labels):
    listol = []
    for label in labels:
        listol.append(label["displayName"])
    return listol

def fetch_labels(token):
    """ Fetch Gmail labels """
    headers = {"Authorization": f"Bearer {token['access_token']}"}
    response = requests.get("https://gmail.googleapis.com/gmail/v1/users/me/labels", headers=headers)
    with open('filteredResponse.json', 'w') as f:
        f.write(str(response.json().get("labels", [])))
    if response.status_code == 200:
        return response.json().get("labels", [])
    else:
        return f"Error fetching labels: {response.status_code}, {response.text}"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
