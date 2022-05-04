import json
import logging
import aiohttp
from data.config import API_URL


CREATE_URL = API_URL + 'basins/create/'
BASINS_LIST = API_URL + 'basins/all/'


def BASIN_DETAIL(basin_id: str) -> str:
    return API_URL + f'basins/{basin_id}/'


def BASIN_UPDATE(basin_id: str) -> str:
    return API_URL + f'basins/{basin_id}/update/'


def basic_auth(user: tuple) -> aiohttp.BasicAuth:
    return aiohttp.BasicAuth(login=user[1], password=user[2])


async def add_basin(user: tuple, data: dict) -> bool:
    auth = basic_auth(user)
    async with aiohttp.ClientSession(auth=auth) as session:
        async with session.post(CREATE_URL, json=data) as resp:
            if resp.status == 201:
                return True
            logging.error(await resp.text())
            return False


async def get_basins_list(user: tuple) -> list:
    auth = basic_auth(user)
    async with aiohttp.ClientSession(auth=auth) as session:
        async with session.get(BASINS_LIST) as resp:
            if resp.status == 200:
                return await resp.json()
            logging.error(await resp.text())
            return []


async def get_basin(user: tuple, basin_id: str) -> dict:
    auth = basic_auth(user)
    async with aiohttp.ClientSession(auth=auth) as session:
        async with session.get(BASIN_DETAIL(basin_id)) as resp:
            if resp.status == 200:
                return await resp.json()
            logging.error(await resp.text())
            return {}


async def set_basin_height(user: tuple, basin_id: str, data: dict) -> dict:
    auth = basic_auth(user)
    async with aiohttp.ClientSession(auth=auth) as session:
        async with session.post(BASIN_UPDATE(basin_id=basin_id), json=data) as resp:
            if resp.status == 200:
                return await resp.json()
            return {}
