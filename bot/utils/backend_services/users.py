# import logging
# import requests
# from data.config import API_URL
#
# CHECK_IS_ALREADY_USER = API_URL + 'users/is-already-user/'
# CHECK_URL = API_URL + 'users/check/'
# CREATE_URL = API_URL + 'users/create/'
# CHANGE_USERNAME_URL = API_URL + 'users/change-username/'
#
#
# async def is_already_user(chat_id: int) -> dict:
#     username = str(chat_id)
#     data = {
#         'username': username
#     }
#     res = requests.post(CHECK_IS_ALREADY_USER, data=data)
#     if res.status_code == 200:
#         return {
#             'is_done': True,
#             'data': res.json()
#         }
#     logging.error(res.text)
#     return {
#         'is_done': False
#     }
#
#
# def check(secret_key: str) -> dict:
#     data = {
#         'secret_key': secret_key
#     }
#     res = requests.post(CHECK_URL, data=data)
#     if res.status_code == 200:
#         return {
#             'is_done': True,
#             'data': res.json()
#         }
#     logging.error(res.text)
#     return {
#         'is_done': False
#     }
#
#
# def create(chat_id: int, data: dict) -> dict:
#     username = str(chat_id)
#     password = str(chat_id)[::-1]
#     data['username'] = username
#     data['password'] = password
#     res = requests.post(CREATE_URL, data=data)
#     if res.status_code == 201:
#         return {
#             'is_done': True,
#             'data': res.json()
#         }
#     logging.error(res.text)
#     return {
#         'is_done': False
#     }
#
#
# def change_username(secret_key: str, chat_id: int) -> dict:
#     username = str(chat_id)
#     data = {
#         'secret_key': secret_key,
#         'username': username
#     }
#     res = requests.post(CHANGE_USERNAME_URL, data=data)
#     if res.status_code == 200:
#         return {
#             'is_done': True,
#             'data': res.json()
#         }
#     logging.error(res.text)
#     return {
#         'is_done': False
#     }
