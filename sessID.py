import requests, hashlib
import os
from dotenv import load_dotenv

load_dotenv()


username=str(os.getenv('username'))
password=str(os.getenv('password'))

def get_sessionid(username, password):
    url = "https://i.instagram.com/api/v1/accounts/login/"

    def generate_device_id(username, password):
        m = hashlib.md5()
        m.update(username.encode() + password.encode())

        seed = m.hexdigest()  
        volatile_seed = "12345"

        m = hashlib.md5()
        m.update(seed.encode('utf-8') + volatile_seed.encode('utf-8'))
        return 'android-' + m.hexdigest()[:16]

    device_id = generate_device_id(username, password)

    payload = {
        'username': username,
        'device_id': device_id,
        'password': password,
    }

    headers = {
        'Accept': '*/*',
        'Content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Accept-Language': 'en-US',
        'User-Agent': "Instagram 10.26.0 Android",
        'referer' : "https://www.instagram.com/accounts/login/"
    }

    response = requests.post(url, headers=headers, data=payload)
    if response.status_code == 200:
        return response.cookies.get_dict()['sessionid']
    
    return response.text

def get_it():
    return get_sessionid(username,password)
