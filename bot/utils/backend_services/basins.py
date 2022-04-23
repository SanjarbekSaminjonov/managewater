# import requests
# from data.config import API_URL
#
#
# def get_session(chat_id: int) -> requests.Session:
#     username = str(chat_id)
#     password = str(chat_id)[::-1]
#     session = requests.Session()
#     session.auth = (username, password)
#     return session
