import os
import sqlite3
import json
import uuid
import threading
import functools
import time
import random
import copy
from typing import List, Dict, Optional, Set, TypeVar

from db.sql_requests import create_tables
# import routes.auth.auth_codes


DB_FILE_NAME = os.path.join('db', 'data.db')
PATH_trackS = os.path.join('db', 'tracks_flac')


def get_part_of_set(collection: Set[TypeVar], amount: int) -> Set[TypeVar]:
    if amount >= len(collection):
        return collection

    result = set()
    while len(result) != amount:
        elem = collection.pop()
        result.add(elem)

    return result


def decorator_locking(method):
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        try:
            self._lock.acquire(True)
            result = method(self, *args, **kwargs)
            self._conn.commit()
        finally:
            self._lock.release()
        return result
    return wrapper


class DBHandler:
    def __init__(self):
        self._conn = sqlite3.connect(DB_FILE_NAME, check_same_thread=False)
        self._cursor = self._conn.cursor()

        self._lock = threading.Lock()

        create_tables(self._cursor)
        self._conn.commit()

    # ==============================================================
    # Search
    def get_search_results(self, search_str: str) -> Dict[str, List[str]]:
        search_str = search_str.lower()
        result = {
            'artists': set(),
            'albums': set(),
            'playlists': set(),
            'tracks': set()
        }

        self._cursor.execute(
            f'SELECT artist_id, artist_name FROM artists '
            f'WHERE INSTR(LOWER(artist_name), ?) > 0 LIMIT 10',
            (search_str,)
        )
        result['artists'] = result['artists']\
            .union(set(self._cursor.fetchall()))

        for artist_id, _ in result['artists']:
            self._cursor.execute(
                f'SELECT album_id, album_artists_id, album_info FROM albums '
                f'WHERE INSTR(LOWER(album_artists_id), ?) > 0 LIMIT 10',
                (artist_id,)
            )
            result['albums'] = result['albums'].union(self._cursor.fetchall())

            self._cursor.execute(
                f'SELECT track_id, track_artists_id, track_album_id, track_info FROM tracks '
                f'WHERE INSTR(LOWER(track_artists_id), ?) > 0 LIMIT 10',
                (artist_id,)
            )
            tracks = self._cursor.fetchall()
            result['tracks'] = result['tracks'].union(
                {random.choice(tracks), random.choice(tracks)}
            )

        self._cursor.execute(
            f'SELECT album_id, album_artists_id, album_info FROM albums '
            f'WHERE INSTR(LOWER(album_info), ?) > 0 LIMIT 10',
            (search_str,)
        )
        result['albums'] = result['albums'].union(set(self._cursor.fetchall()))

        self._cursor.execute(
            f'SELECT playlist_id, playlist_authors_id, playlist_info FROM playlists '
            f'WHERE INSTR(LOWER(playlist_info), ?) > 0 LIMIT 10',
            (search_str,)
        )
        result['playlists'] = result['playlists']\
            .union(set(self._cursor.fetchall()))

        self._cursor.execute(
            f'SELECT track_id, track_artists_id, track_album_id, track_info FROM tracks '
            f'WHERE INSTR(LOWER(track_info), ?) > 0 LIMIT 10',
            (search_str,)
        )
        result['tracks'] = result['tracks'].union(set(self._cursor.fetchall()))

        # print(result)
        result['artists'] = get_part_of_set(result['artists'], 3)
        result['albums'] = get_part_of_set(result['albums'], 3)
        result['playlists'] = get_part_of_set(result['playlists'], 3)
        result['tracks'] = get_part_of_set(result['tracks'], 6)

        for key in result.keys():
            result[key] = list(result[key])
        return result

    # ==============================================================
    # Artists
    @decorator_locking
    def get_artist_name(self, artist_id: str) -> Optional[str]:
        self._cursor.execute(
            'SELECT artist_name FROM artists WHERE artist_id=?',
            (artist_id, )
        )
        result = self._cursor.fetchone()
        return result[0] if result is not None else None

    @decorator_locking
    def get_artist_info(self, artist_id: str) -> Optional[str]:
        self._cursor.execute(
            'SELECT artist_info FROM artists WHERE artist_id=?',
            (artist_id, )
        )
        result = self._cursor.fetchone()
        return result[0] if result is not None else None

    @decorator_locking
    def get_artist_picture_path(self, artist_id: str) -> Optional[str]:
        self._cursor.execute(
            'SELECT artist_picture_path FROM artists WHERE artist_id=?',
            (artist_id,)
        )
        result = self._cursor.fetchone()
        return result[0] if result is not None else None

    @decorator_locking
    def get_artist_albums(self, artist_id: str) -> Optional[List[str]]:
        self._cursor.execute(
            'SELECT artist_albums FROM artists WHERE artist_id=?',
            (artist_id, )
        )
        result = self._cursor.fetchone()
        return json.loads(result[0]) if result is not None else None

    @decorator_locking
    def get_artist_tracks(self, artist_id: str) -> Optional[List[str]]:
        self._cursor.execute(
            'SELECT artist_tracks FROM artists WHERE artist_id=?',
            (artist_id, )
        )
        result = self._cursor.fetchone()
        return json.loads(result[0]) if result is not None else None

    # ==============================================================
    # Albums
    @decorator_locking
    def get_album_artists(self, album_id: str) -> Optional[List[str]]:
        self._cursor.execute(
            'SELECT album_artists_id FROM albums WHERE album_id=?',
            (album_id, )
        )
        result = self._cursor.fetchone()
        return json.loads(result[0]) if result is not None else None

    @decorator_locking
    def get_album_info(self, album_id: str) -> Optional[Dict[str, str]]:
        self._cursor.execute(
            'SELECT album_info FROM albums WHERE album_id=?',
            (album_id, )
        )
        result = self._cursor.fetchone()
        return json.loads(result[0]) if result is not None else None

    @decorator_locking
    def get_album_picture_path(self, album_id: str) -> Optional[str]:
        self._cursor.execute(
            'SELECT album_picture_path FROM albums WHERE album_id=?',
            (album_id,)
        )
        result = self._cursor.fetchone()
        return result[0] if result is not None else None

    @decorator_locking
    def get_album_tracks(self, album_id: str) -> Optional[List[str]]:
        self._cursor.execute(
            'SELECT album_tracks FROM albums WHERE album_id=?',
            (album_id, )
        )
        result = self._cursor.fetchone()
        return json.loads(result[0]) if result is not None else None

    # ==============================================================
    # Playlists
    @decorator_locking
    def get_playlist_authors(self, playlist_id: str) -> Optional[List[str]]:
        self._cursor.execute(
            'SELECT playlist_artists_id FROM playlists WHERE playlist_id=?',
            (playlist_id, )
        )
        result = self._cursor.fetchone()
        return json.loads(result[0]) if result is not None else None

    @decorator_locking
    def get_playlist_info(self, playlist_id: str) -> Optional[Dict[str, str]]:
        self._cursor.execute(
            'SELECT playlist_info FROM playlists WHERE playlist_id=?',
            (playlist_id, )
        )
        result = self._cursor.fetchone()
        return json.loads(result[0]) if result is not None else None

    @decorator_locking
    def get_playlist_picture_path(self, playlist_id: str) -> Optional[str]:
        self._cursor.execute(
            'SELECT playlist_picture_path FROM playlists WHERE playlist_id=?',
            (playlist_id,)
        )
        result = self._cursor.fetchone()
        return result[0] if result is not None else None

    @decorator_locking
    def get_playlist_tracks(self, playlist_id: str) -> Optional[List[str]]:
        self._cursor.execute(
            'SELECT playlist_tracks FROM playlists WHERE playlist_id=?',
            (playlist_id, )
        )
        result = self._cursor.fetchone()
        return json.loads(result[0]) if result is not None else None

    # ==============================================================
    # Tracks
    @decorator_locking
    def get_track_artists(self, track_id: str) -> Optional[List[str]]:
        self._cursor.execute(
            'SELECT track_artists_id FROM tracks WHERE track_id=?',
            (track_id, )
        )
        result = self._cursor.fetchone()
        return json.loads(result[0]) if result is not None else None

    @decorator_locking
    def get_track_album(self, track_id: str) -> Optional[str]:
        self._cursor.execute(
            'SELECT track_album_id FROM tracks WHERE track_id=?',
            (track_id, )
        )
        result = self._cursor.fetchone()
        return result[0] if result is not None else None

    @decorator_locking
    def get_track_info(self, track_id: str) -> Optional[Dict[str, str]]:
        self._cursor.execute(
            'SELECT track_info FROM tracks WHERE track_id=?',
            (track_id, )
        )
        result = self._cursor.fetchone()
        return json.loads(result[0]) if result is not None else None

    @decorator_locking
    def get_track_path(self, track_id: str) -> Optional[str]:
        self._cursor.execute(
            'SELECT track_path FROM tracks WHERE track_id=?',
            (track_id, )
        )
        result = self._cursor.fetchone()
        return result[0] if result is not None else None

    # ==============================================================
    # Users
    @decorator_locking
    def add_user(self, login: str, password: str, email: str, photo: bytes) -> \
            int:
        self._cursor.execute(
            'SELECT user_auth_key FROM users '
            'WHERE user_login=?',
            (login,)
        )
        result = self._cursor.fetchone()
        if result is None:
            return 1

        user_id = str(uuid.uuid4())
        user_auth_key = str(uuid.uuid4())
        self._cursor.execute(
            'INSERT INTO users '
            '(user_id, user_login, user_password, user_email, user_auth_key,'
            'user_photo, user_artists, user_playlists, user_subscription) '
            'VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)',
            (user_id, login, password, email, user_auth_key, photo, '',
             '', 0)
        )
        self._conn.commit()
        return 0

    @decorator_locking
    def check_user_auth(self, login: str, password: str) -> Optional[str]:
        self._cursor.execute(
            'SELECT user_auth_key FROM users '
            'WHERE user_login=? AND user_password=?',
            (login, password)
        )
        result = self._cursor.fetchone()
        return result[0] if result is not None else None

    @decorator_locking
    def check_user_auth_key(self, auth_key: str) -> bool:
        self._cursor.execute(
            'SELECT user_id FROM users WHERE user_auth_key=?',
            (auth_key,)
        )
        result = self._cursor.fetchone()
        return result is not None

    @decorator_locking
    def get_user(self, auth_key: str) -> Optional[tuple[str, str, str, str]]:
        self._cursor.execute(
            'SELECT user_login, user_email, user_birth, user_country '
            'FROM users WHERE user_auth_key=?',
            (auth_key,)
        )
        result = self._cursor.fetchone()
        return result if result is not None else None

    @decorator_locking
    def get_user_id(self, auth_key: str) -> Optional[str]:
        self._cursor.execute(
            'SELECT user_id FROM users WHERE user_auth_key=?',
            (auth_key,)
        )
        result = self._cursor.fetchone()
        return result[0] if result is not None else None

    @decorator_locking
    def get_user_login(self, auth_key: str) -> Optional[str]:
        self._cursor.execute(
            'SELECT user_login FROM users WHERE user_auth_key=?',
            (auth_key,)
        )
        result = self._cursor.fetchone()
        return result[0] if result is not None else None

    @decorator_locking
    def check_user_email(self, email: str) -> bool:
        self._cursor.execute(
            'SELECT user_email FROM users WHERE user_email=?',
            (email,)
        )
        result = self._cursor.fetchone()
        return result is not None

    @decorator_locking
    def set_user_password(self, reset_code: str, password: str) -> bool:
        self._cursor.execute(
            'SELECT user_email FROM reset_codes WHERE reset_code=?',
            (reset_code,)
        )
        result = self._cursor.fetchone()
        if result is None:
            return False
        user_email = result[0]

        self._cursor.execute(
            'UPDATE users SET user_password=? WHERE user_email=?',
            (password, user_email)
        )
        self._cursor.execute(
            'DELETE FROM reset_codes WHERE reset_code=?',
            (reset_code,)
        )
        return True

    @decorator_locking
    def get_user_photo(self):
        pass

    @decorator_locking
    def get_user_artists(self, user_id: str) -> Optional[List[str]]:
        self._cursor.execute(
            'SELECT user_artists_id FROM users WHERE user_id=?',
            (user_id,)
        )
        result = self._cursor.fetchone()
        return json.loads(result[0]) if result is not None else None

    @decorator_locking
    def get_user_playlists(self, user_id: str) -> Optional[List[str]]:
        self._cursor.execute(
            'SELECT user_playlists FROM users WHERE user_id=?',
            (user_id,)
        )
        result = self._cursor.fetchone()
        return json.loads(result[0]) if result is not None else None

    @decorator_locking
    def get_user_subscription(self, user_id: str) -> Optional[int]:
        self._cursor.execute(
            'SELECT user_subscription FROM users WHERE user_id=?',
            (user_id,)
        )
        result = self._cursor.fetchone()
        return int(result[0]) if result is not None else None

    @decorator_locking
    def get_user_last_track_id(self, user_id: str) -> Optional[str]:
        self._cursor.execute(
            'SELECT last_track_id FROM users WHERE user_id=?',
            (user_id,)
        )
        result = self._cursor.fetchone()
        return result[0] if result is not None else None

    @decorator_locking
    def update_user_last_track_id(self, user_id: str, last_track_id: str) -> None:
        self._cursor.execute(
            'UPDATE users SET last_track_id = ? WHERE user_id=?',
            (last_track_id, user_id,)
        )

    # ==============================================================
    # Reset Codes
    @decorator_locking
    def set_reset_code(self, user_email: str) -> Optional[str]:
        code = str(uuid.uuid4())

        self._cursor.execute(
            'INSERT INTO reset_codes '
            '(reset_code, user_email, reset_code_time_expire) '
            'VAlUES (?, ?, ?)',
            (code, user_email, time.time() + 86400)  # 86400 sec = 1 day
        )
        return code

    @decorator_locking
    def check_reset_code(self, reset_code: str) -> Optional[str]:
        self._cursor.execute(
            'SELECT user_email, reset_code_time_expire FROM reset_codes WHERE reset_code=?',
            (reset_code,)  # 86400 sec = 1 day
        )
        result = self._cursor.fetchone()
        if result is None:
            return None
        user_email, reset_code_time_expire = result

        if int(float(reset_code_time_expire)) < time.time():
            return None

        return user_email
