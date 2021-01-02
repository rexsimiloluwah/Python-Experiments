import requests
import os
import argparse
import json

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--endpoint", required = True, help = "Endpoint on the Base URL")
args = vars(ap.parse_args())


def get_data(endpoint):
    
    BASE_URL = "http://localhost:8000/"
    url = os.path.join(BASE_URL, endpoint)
    print(url)
    r = requests.get(url)

    if r.status_code != requests.codes.ok:
        return None
    return r.json()

def post_data(endpoint):
    BASE_URL = "http://localhost:8000/"
    url = os.path.join(BASE_URL, endpoint)
    print(url)

    data = {
        "title" : "Last Christmas", 
        "description" : "A movie where a lady fell in love with a ghost on christmas day",
        "rating" : 5, 
        "year" : 2019
    }

    r = requests.post(url, data = data)
    print(r.headers)
    print(r.text)
    if (r.status_code != requests.codes.ok):
        return None
    return r.json()


def update_data(endpoint):
    BASE_URL = "http://localhost:8000/"
    url = os.path.join(BASE_URL, endpoint)
    print(url)
    new_data = {
        "title" : "Last Christmas 2", 
        "description" : "A movie where a lady fell in love with a ghost on christmas day"
    }

    r = requests.put(url, data = json.dumps(new_data) )
    print(r.headers)
    print(r.text)
    if (r.status_code != requests.codes.ok):
        return None
    return r.json()

def delete_data(endpoint):
    BASE_URL = "http://localhost:8000/"
    url = os.path.join(BASE_URL, endpoint)
    print(url)
    r = requests.delete(url)
    print(r.headers)
    print(r.text)
    if (r.status_code != requests.codes.ok):
        return None
    return r.json()


print(delete_data(args["endpoint"]))