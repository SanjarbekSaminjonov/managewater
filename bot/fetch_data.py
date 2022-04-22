import requests
from data.config import API_URL

SIGN_UP_URL = API_URL + 'users/signup/'


def signup_user(data=None):
    res = requests.get(SIGN_UP_URL)
    return res


if __name__ == '__main__':
    res = signup_user()
    if res.status_code == 200:
        print(res.json())
