import re
import requests

from datetime import datetime

link = 'https://www.instagram.com/accounts/login/'
login_url = 'https://www.instagram.com/accounts/login/ajax/'
def get_SessionID():
    
    time = int(datetime.now().timestamp())

    payload = {
        'username': '',
        'enc_password': f'#PWD_INSTAGRAM_BROWSER:0:{time}:<PASSWORD HERE>',
        'queryParams': {},
        'optIntoOneTap': 'false'
    }

    with requests.Session() as s:
        r = s.get(link)
        csrf = re.findall(r"csrf_token\":\"(.*?)\"",r.text)[0]
        r = s.post(login_url,data=payload,headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36",
            "X-Requested-With": "XMLHttpRequest",
            "Referer": "https://www.instagram.com/accounts/login/",
            "x-csrftoken":csrf
        })
        print(r.status_code)
        print(r.url)
        print(r.text)

        print(s.cookies)
