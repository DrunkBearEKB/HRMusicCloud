import sqlite3
import uuid


DB_FILE_NAME = 'db/users_db/users.db'


class UsersDBHandler:
    def __init__(self):
        self._conn = sqlite3.connect(DB_FILE_NAME, check_same_thread=False)
        self._cursor = self._conn.cursor()

        self._cursor.execute(
            "CREATE TABLE IF NOT EXISTS users "
            "(user_id text, login text, password text, subscription integer)"
        )
        self._conn.commit()

    def add_user(self, login: str, password: str, subscription: str) -> str:
        user_id = str(uuid.uuid4())
        self._cursor.execute(
            f"INSERT INTO users VALUES "
            f"()",
            (user_id, login, password)
        )
        self._conn.commit()

        return user_id

    def remove_user(self, user_id: str):
        self._cursor.execute(
            f"DELETE FROM users WHERE user_id = '{user_id}'"
        )
        self._conn.commit()

    def update_password(self, user_id: str, password_new: str):
        self._cursor.execute(
            f"UPDATE users SET password = '{password_new}' "
            f"WHERE user_id = '{user_id}'"
        )
        self._conn.commit()

    def update_subscription(self, user_id: str, subscription__new: str):
        self._cursor.execute(
            f"UPDATE users SET subscription = '{subscription__new}' "
            f"WHERE user_id = '{user_id}'"
        )
        self._conn.commit()
