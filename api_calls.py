from flask_login import current_user
from flask import flash
import requests
from app import db

# Function to log in to BAM PI, logs in and returns the api token
def api_login(host, useraccount, userpassword):
    url = "http://{0}/Services/REST/v1/login?".format(host)
    params = {"username": useraccount, "password": userpassword}
    response = requests.get(url, params=params)
    if (response.status_code) != 200:
        return response.text
    else:
        return response.json()

def try_login(host, username, password):
    try:
        raw_token = api_login(host, username, password)
        return raw_token
    except:
        return flash("Server Unreachable!")

def getSystemInfo(token, host):
    url = "http://{0}/Services/REST/v1/getSystemInfo".format(host)
    headers = {
        'Authorization': token,
        'Content-Type': "application/json"
    }
    response = requests.get(url, headers=headers)
    if (response.status_code) != 200:
        return response.text
    else:
        return response.json()