from flask import Flask, request, redirect, url_for, session, jsonify
from requests_oauthlib import OAuth2Session
import os
from dotenv import load_dotenv
import requests
import json
from cryptography.fernet import Fernet

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
app.config["SECRET_KEY"] = SECRET_KEY
oauth = OAuth2Session(CLIENT_ID, redirect_uri=REDIRECT_URI, scope=SCOPES)


@app.route("/")
def home():
    """ Redirect users to Google OAuth """
    return f'<a>Backend</a>'

@app.route("/authredirect")
def authRedirect():
    """ Redirect users to Google OAuth """
    auth_url, _ = oauth.authorization_url(AUTH_URL)
    return redirect(auth_url)

@app.route("/OLDsuccess")
def OLDsuccess(labels=None):
    data = request.args.get("data", "[]")
    labels = json.loads(data)
    return f"<a>Success! Check out the terminal</a> </br> <a> List of labels = {listOfLabels(labels)}</a>"

@app.route("/success")
def success():
    return f"<a>Token saved in session cookies</a>"

@app.route("/retrievetoken")  #!!!!!!
def retrieveToken():
    return jsonify({"token":session.get("token")}), 401 if session.get("token") == "no token" else 200

@app.route("/checktoken")
def checkToken():
    encrypted_token = request.cookies.get("authToken")

    if encrypted_token:
        decrypted_token = cipher.decrypt(encrypted_token.encode()).decode()  # Decrypt token
        return f"Decrypted Token: {decrypted_token}", 200
    else:
        return "No token found", 401


@app.route("/callback")
def callback():
    """ Handle OAuth callback and fetch emails """
    token = oauth.fetch_token(TOKEN_URL, client_secret=CLIENT_SECRET, authorization_response=request.url)

    if token:
        encryptedToken = CIPHER.encrypt(token.encode())
        response.make_response("")
        response.set_cookie("authToken", encryptedToken, httponly=True, secure= True if os.name != "nt" else False, samesite="Strict")

        # return redirect("localhost:3000/auth") # ! Hard coded redirect, needs start url instead
        return redirect(url_for("success"))  # Redirect to success page
    else:
        return jsonify({"error": "Failed to retrieve token"}), 401  # Return error if no token

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
