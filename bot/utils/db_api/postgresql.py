import asyncpg
from typing import Union
from data import config


class Database:

    def __init__(self):
        self.pool: Union[asyncpg.pool.Pool, None] = None

    async def create_pool(self):
        self.pool = await asyncpg.create_pool(
            user=config.DB_USER,
            password=config.DB_PASS,
            host=config.DB_HOST,
            database=config.DB_NAME
        )

    async def execute(self, command, *args, fetch: bool = False,
                      fetchval: bool = False, fetchrow: bool = False, execute: bool = False):
        async with self.pool.acquire() as connection:
            connection: asyncpg.Connection
            async with connection.transaction():
                if fetch:
                    result = await connection.fetch(command, *args)
                elif fetchval:
                    result = await connection.fetchval(command, *args)
                elif fetchrow:
                    result = await connection.fetchrow(command, *args)
                elif execute:
                    result = await connection.execute(command, *args)
            return result

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ${num}" for num, item in enumerate(parameters.keys(), start=1)
        ])
        return sql, tuple(parameters.values())

    async def get_user(self, **kwargs):
        sql = 'SELECT * FROM users_customuser WHERE '
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)

    async def check_basin_is_exist(self, basin_id):
        sql = 'SELECT * FROM basins_basinid WHERE id = $1'
        return await self.execute(sql, basin_id, fetchrow=True)

    async def add_basin(self, data):

        id = data.get('id')
        phone = data.get('phone')
        name = data.get('name')
        height = data.get('height')
        latitude = data.get('latitude', None)
        longitude = data.get('longitude', None)
        belong_to_id = data.get('belong_to_id')

        conf_height = 0

        sql = '''
            INSERT INTO
                basins_basin (id, phone, name, height, latitude, longitude, belong_to_id, conf_height)
            VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
        '''
        return await self.execute(
            sql, id, phone, name, height, latitude, longitude, belong_to_id, conf_height, execute=True)

    async def get_basin_by_id(self, basin_id):
        sql = 'SELECT * FROM basins_basin WHERE id = $1'
        return await self.execute(sql, basin_id, fetchrow=True)

    async def get_user_basins(self, user_id):
        sql = 'SELECT * FROM basins_basin WHERE belong_to_id = $1'
        return await self.execute(sql, user_id, fetch=True)

    async def get_basins(self):
        sql = 'SELECT * FROM basins_basin'
        return await self.execute(sql, fetch=True)

    async def update_basin_main_height(self, basin_id, height):
        sql = 'UPDATE basins_basin SET height = $1 WHERE id = $2'
        return await self.execute(sql, height, basin_id, execute=True)

    async def update_basin_conf_height(self, basin_id, conf_height):
        sql = 'UPDATE basins_basin SET conf_height = $1 WHERE id = $2'
        return await self.execute(sql, conf_height, basin_id, execute=True)

    async def get_basin_last_message(self, basin_id):
        sql = 'SELECT * FROM basins_basinmessage WHERE basin_id = $1 ORDER BY id DESC LIMIT 1'
        return await self.execute(sql, basin_id, fetchrow=True)

    async def get_basin_messages_between_dates(self, basin_id, start_date, end_date):
        sql = 'SELECT * FROM basins_basinmessage WHERE basin_id = $1 AND created_at between $2 and $3'
        return await self.execute(sql, basin_id, start_date, end_date, fetch=True)

    async def get_basin_messages_after_date(self, basin_id, start_date):
        sql = 'SELECT * FROM basins_basinmessage WHERE basin_id = $1 AND created_at >= $2'
        return await self.execute(sql, basin_id, start_date, fetch=True)

    async def get_basin_messages_before_date(self, basin_id, end_date):
        sql = 'SELECT * FROM basins_basinmessage WHERE basin_id = $1 AND created_at <= $2'
        return await self.execute(sql, basin_id, end_date, fetch=True)

    async def get_basin_messages(self, basin_id):
        sql = 'SELECT * FROM basins_basinmessage WHERE basin_id = $1 ORDER BY created_at'
        return await self.execute(sql, basin_id, fetch=True)

    async def add_additional_watcher(self, basin_id, watcher_id):
        sql = 'INSERT INTO basins_additionalwatcher (basin_id, watcher_id) VALUES ($1, $2)'
        return await self.execute(sql, basin_id, watcher_id, execute=True)

    async def get_additional_watcher(self, basin_id, watcher_id):
        sql = 'SELECT * FROM basins_additionalwatcher WHERE basin_id = $1 AND watcher_id = $2'
        return await self.execute(sql, basin_id, watcher_id, fetchrow=True)

    async def get_watched_basins_by_user(self, basin_id):
        sql = 'SELECT * FROM basins_additionalwatcher WHERE watcher_id = $1'
        return await self.execute(sql, basin_id, fetch=True)
