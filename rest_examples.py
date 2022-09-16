import requests
import datetime
import csv
from time import sleep

def login(host, useraccount, userpassword):
    url = "http://{0}/Services/REST/v1/login?".format(host)
    params = {"username":useraccount,"password":userpassword}
    response = requests.get(url, params=params)
    if (response.status_code) != 200:
        print(response.status_code)
        return response.text
    else:
        return response.json()


def logout(token, host):
    url = "http://{0}/Services/REST/v1/logout?".format(host)
    headers = {
        'Authorization': token,
    }
    response = requests.get(url, headers=headers)
    if (response.status_code) != 200:
        return response.text
    else:
        return response.json()


def gettoken(data):
    token = data.split()[2] + " " + data.split()[3]
    return token


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


def getEntities(token, host, parentId, entitytype):
    url = "http://{0}/Services/REST/v1/getEntities?".format(host)
    headers = {
        'Authorization': token,
        'Content-Type': "application/json"
    }

    querystring = {'parentId': parentId, 'type': entitytype, 'start': 0, 'count': 100}

    response = requests.get(url, headers=headers, params=querystring)
    if (response.status_code) != 200:
        return response.text
    else:
        return response.json()

def searchByCategory(token, host, keyword, category):
    url = "http://{0}/Services/REST/v1/searchByCategory?".format(host)
    headers = {
        'Authorization': token,
        'Content-Type': "application/json"
    }

    querystring = {'keyword': keyword, 'category': category, 'start': 0, 'count': 10000}

    response = requests.get(url, headers=headers, params=querystring)
    if (response.status_code) != 200:
        return response.text
    else:
        return response.json()

def selectiveDeploy(token, host, hostids):
    url = "http://{0}/Services/REST/v1/selectiveDeploy?".format(host)
    headers = {
        'Authorization': token,
        'Content-Type': "application/json"
    }

    # one single id
    if isinstance(hostids,int):
        hostids = [hostids]

    # string containing one or multiple ids comma separated
    elif isinstance(hostids,str):
        ids = hostids.split(",")
        hostids = [int(i) for i in ids]

    # if list
    elif isinstance(hostids, list):
        pass

    else:
        raise ValueError("entityIds must be a one id, a list of ids or a string of comma separated ids. {} found".format(type(hostids)))

    payload = str(hostids)
    params = {'properties':''}
    response = requests.post(url, headers=headers, data=payload, params=params)
    if (response.status_code) != 200:
        return response.text
    else:
        return response.json()    



# host = "192.168.245.10"
host = "192.168.245.9"
user, passwd = ("apiuser", "apiuser")
info = login(host, user, passwd)
token = gettoken(info)

system_info = getSystemInfo(token, host)
print(system_info)

print(selectiveDeploy(token, host, [12345]))

logout(token, host)