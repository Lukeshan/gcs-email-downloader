from flask import Flask, request, redirect, url_for, session, jsonify
from requests_oauthlib import OAuth2Session
import os
from dotenv import load_dotenv
import requests
import json
from cryptography.fernet import Fernet
from flask_cors import CORS

    

app = Flask(__name__)
CORS(app)
@app.route("/")
def home():
    """ Redirect users to Google OAuth """
    return f'<a>Backend</a>'

@app.route("/test")
def test():
    value = input("Input value(str): ")

    if value in ["lukeshan","daniel","connor"]:
        return jsonify({"name":value,"success":True}),200
    else:
        return jsonify({"statusText":"not resident","success":False}),400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
