import logging
import aiohttp
from data.config import API_URL


CREATE_URL = API_URL + 'users/create/'


async def register(data: dict) -> bool:
    async with aiohttp.ClientSession() as session:
        async with session.post(CREATE_URL, json=data) as resp:
            if resp.status == 201:
                return True
            logging.error(await resp.text())
            return False
