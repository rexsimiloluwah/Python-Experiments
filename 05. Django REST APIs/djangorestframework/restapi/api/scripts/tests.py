# Scripts for testing the API endpoints

import requests
import os
import json
BASE_URL = "http://localhost:8000/"


image_path = os.path.join(os.getcwd(), "assets/arduino-board.jpg")

def call(method = "get", data = {}, id = None, img_path = None):
    r = requests.request(method = method, url= os.path.join(BASE_URL, f"api/posts/{id}"), data = data)
    print(r.text)
    if r.status_code != requests.codes.ok:
        return None
    return r.json()

def post(method = "post", data = {}, is_json = True,  img_path = None):
    headers = {}
    if is_json: 
        headers["content-type"] = "application/json"
        data = json.dumps(data)
    
    if img_path is not None:
        with open(img_path, "rb") as image:
            file_data = {
                "post_image" : image
            }
            r = requests.request(method = method, url = os.path.join(BASE_URL, f"api/posts/"), data = data, files = file_data )

    if r.status_code != requests.codes.ok:
        return None
    else: 
        return r.json()


def put(method = "put", data = {}, id = None, is_json = True, img_path = None):
    headers = {}
    if is_json:
        headers["content-type"] = "application/json"
        data = json.dumps(data)

    if img_path is not None:
        with open(img_path, "rb") as image:
            file_data = {
                "post_image" : image
            }
            r = requests.request(method = method, url = os.path.join(BASE_URL, f"api/posts/{id}"), data = data, files = file_data)

    if r.status_code != requests.codes.ok:
        return None
    else: 
        return r.json()


# JWT Authentication ENDPOINT
AUTH_VIEW_ENDPOINT = os.path.join(BASE_URL, "api/auth/")
AUTH_REGISTER_ENDPOINT = os.path.join(BASE_URL, "api/auth/serializedregister/")
AUTH_END_POINT = os.path.join(BASE_URL, "api/auth/jwt/")
REFRESH_END_POINT = os.path.join(AUTH_END_POINT, "refresh/")

def jwt(data = {}):
    # The JWT Authentication only works with POST Requests !
    r = requests.post(AUTH_END_POINT, data = data)
    if r.status_code != requests.codes.ok:
        return None
    return r.json()

def refresh_jwt( data = {}):
    # The endpoint for refreshing the already generated JWT token for authentication 
    data = json.dumps(data)
    headers = {
        "Content-type" : "application/json",
    }
    r = requests.post(REFRESH_END_POINT, data = data, headers = headers)
    if r.status_code != requests.codes.ok:
        return None
    return r.json()


data = {
    "username" : "random4",
    "email" : "random4@gmail.com",
    "password" : "adetoyosi",
    "password2" : "adetoyosi"
}

headers = {
    "Content-type" : "application/json",
    "Authorization" : "JWT "+"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjo3LCJ1c2VybmFtZSI6InJhbmRvbTMiLCJleHAiOjE2MDA2NTE0NTcsImVtYWlsIjoicmFuZG9tM0BnbWFpbC5jb20iLCJvcmlnX2lhdCI6MTYwMDY1MTE1N30.13HhLhxf6miDbp1pdkwjBXPniCeeYziAiSRgdi6bMmo"
}

r = requests.post(AUTH_REGISTER_ENDPOINT, data = json.dumps(data), headers = headers)
print(r.json())


# token = jwt(data = {
#     "username" : "theblackdove", 
#     "password" : "adetoyosi"
# })

# token = token["token"]

# new_token = refresh_jwt(
#     data = {
#         "token" : token,
#     }
# )

    


# put(data = {
#     "user" : 1,
#     "content" : "[EDITED]:- Corona Virus is a novel virus ravaging the current state of the world, it's outbreak has further led to a worldwide pandemic !"
# }, is_json = False, img_path = image_path, id = 5)

# call(id = 6)