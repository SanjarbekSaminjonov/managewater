import sqlite3


class Database:
    def __init__(self, path_to_db="main.db"):
        self.path_to_db = path_to_db

    def create_table_users(self):
        sql = """
        CREATE TABLE users (
            chat_id int NOT NULL,
            username varchar(255) NOT NULL,
            password varchar(255),
            PRIMARY KEY (chat_id)
            );
    """
        self.execute(sql, commit=True)

    @property
    def connection(self):
        return sqlite3.connect(self.path_to_db)

    def execute(self, sql: str, parameters: tuple = None, fetchone=False, commit=False):
        if not parameters:
            parameters = ()
        connection = self.connection
        connection.set_trace_callback(logger)
        cursor = connection.cursor()
        data = None
        cursor.execute(sql, parameters)

        if commit:
            connection.commit()
        if fetchone:
            data = cursor.fetchone()
        connection.close()
        return data

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ?" for item in parameters
        ])
        return sql, tuple(parameters.values())

    def add_user(self, chant_id: int, username: str, password: str):
        sql = "INSERT INTO users (chat_id, username, password) VALUES(?, ?, ?)"
        self.execute(sql, parameters=(chant_id, username, password), commit=True)

    def select_user(self, **kwargs):
        sql = "SELECT * FROM users WHERE "
        sql, parameters = self.format_args(sql, kwargs)
        return self.execute(sql, parameters=parameters, fetchone=True)

    def update_user_chat_id(self, chat_id, username, password):
        sql = f"""
        UPDATE users SET chat_id=? WHERE username=? AND password=?
        """
        return self.execute(sql, parameters=(chat_id, username, password), commit=True)


def logger(statement):
    print(
        f"""
_____________________________________________________        
Executing: 
{statement}
_____________________________________________________
"""
    )

