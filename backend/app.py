from flask import Flask, request, redirect, url_for, session, jsonify, Response
from requests_oauthlib import OAuth2Session
import os
from dotenv import load_dotenv
import requests
import json
from cryptography.fernet import Fernet
from flask_session import Session
from flask_cors import CORS

# Enable HTTPS enforcement
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "0"

# OAuth 2.0 Credentials from Environment Variables
load_dotenv()
ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY")  # Load key securely
CIPHER  = Fernet(ENCRYPTION_KEY)
SECRET_KEY = os.urandom(24)

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
CORS(app)
app.config["SECRET_KEY"] = SECRET_KEY
app.config["SESSION_TYPE"] = "filesystem"  # Stores session data on disk
app.config["SESSION_PERMANENT"] = True
app.config["PERMANENT_SESSION_LIFETIME"] = 3600  # Keeps session alive for 1 hour
app.config["SESSION_FILE_DIR"] = "./.flask_session"
app.config["SESSION_USE_SIGNER"] = True
app.config["SESSION_COOKIE_HTTPONLY"] = True  # Makes cookie inaccessible to JavaScript
app.config["SESSION_COOKIE_SECURE"] =  False  # Forces HTTPS-only
Session(app)
oauth = OAuth2Session(CLIENT_ID, redirect_uri=REDIRECT_URI, scope=SCOPES)


@app.route("/")
def home():
    """ Redirect users to Google OAuth """
    return f'<a>Backend</a>'

@app.route("/authredirect")
def authRedirect():
    """ Redirect users to Google OAuth """
    session["returnUrl"] = request.args.get("redirect_url", "/success")  # Fallback if not provided
    auth_url, _ = oauth.authorization_url(AUTH_URL)
    return redirect(auth_url)

@app.route("/success")
def success():
    return f"<a>Token saved in session cookies. Return to the original webpage</a>"

@app.route("/listlabels")
def returnListOfLabels():
    print(f"Session: {dict(session)}")
    encrypted_token = session.get("loginToken",None)
    print(f"Enc Token: {encrypted_token}")
    if encrypted_token:
        decrypted_token = CIPHER.decrypt(encrypted_token.encode()).decode()  # Decrypt token
    else:
        return "No token found", 401

    labels = fetch_labels(decrypted_token)
    labels = betterLabels(labels)
    return jsonify({"labels":listLabels(labels)}), 200

def betterLabels(rawLabels):
    for label in rawLabels:
        label["displayName"] = label["name"].lower().replace("_"," ").title()
    return rawLabels

def listLabels(labels):
    listol = []
    for label in labels:
        listol.append(label["displayName"])
    return listol

def fetch_labels(token):
    """ Fetch Gmail labels """
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get("https://gmail.googleapis.com/gmail/v1/users/me/labels", headers=headers)
    if response.status_code == 200:
        return response.json().get("labels", [])
    else:
        return "failed"

@app.route("/checktoken")
def checkToken():
    encrypted_token = session.get("loginToken")

    if encrypted_token:
        decrypted_token = CIPHER.decrypt(encrypted_token.encode()).decode()  # Decrypt token
        return f"Decrypted Token: {decrypted_token}", 200
    else:
        return "No token found", 401


@app.route("/callback")
def callback():
    """ Handle OAuth callback and fetch emails """
    token = oauth.fetch_token(TOKEN_URL, client_secret=CLIENT_SECRET, authorization_response=request.url)

    if token:
        token = token["access_token"]
        encryptedToken = CIPHER.encrypt(token.encode())
        session["loginToken"] = encryptedToken.decode()
        returnUrl = session.get("returnUrl",False)
        print(f"Session: {dict(session)}")
        print(f"Request Cookies: {request.cookies}")
        session.modified = True
        return redirect(returnUrl if returnUrl else "/success")  # Redirect to success page
    else:
        return jsonify({"error": "Failed to retrieve token"}), 401  # Return error if no token


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
