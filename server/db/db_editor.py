import sqlite3
import uuid
import json
import sys
import os
from tinytag import TinyTag

from db.sql_requests import create_tables


DB_FILE_NAME = 'data.db'
DIR_TRACKS = 'tracks'
FILE_ARTIST_INFO = 'artist_info.json'
FILE_ARTIST_PICTURE = 'picture.jpg'
FILE_ALBUM_INFO = 'album_info.json'
FILE_ALBUM_PICTURE = 'picture.jpg'
FILE_ALBUM_CHECKED = 'checked'

SKIP_CHECKED = False
REMOVE_PREVIOUS_DB = True


def main():
    if os.path.exists('albums.txt'):
        os.remove('albums.txt')

    file = open('albums.txt', mode='a')

    if REMOVE_PREVIOUS_DB and os.path.exists(DB_FILE_NAME):
        os.remove(DB_FILE_NAME)

    conn = sqlite3.connect(DB_FILE_NAME, check_same_thread=False)
    cursor = conn.cursor()

    create_tables(cursor)
    conn.commit()

    for dir_artist in os.listdir(DIR_TRACKS):
        cursor.execute(
            'SELECT artist_id FROM artists WHERE artist_name=?',
            (dir_artist, )
        )
        artist_id = cursor.fetchone()
        artist_id = str(uuid.uuid4()) if artist_id is None else artist_id

        path_artist = os.path.join(DIR_TRACKS, dir_artist)

        paths_in_artist = os.listdir(path_artist)
        paths_in_artist.remove(FILE_ARTIST_INFO)
        paths_in_artist.remove(FILE_ARTIST_PICTURE)

        with open(os.path.join(path_artist, FILE_ARTIST_INFO), mode='r') \
                as file_artist_info:
            artist_info = json.load(file_artist_info)
        artist_name = artist_info['name']
        # artist_info.pop('name')
        artist_picture_path = os.path.join(
            'db', path_artist, FILE_ARTIST_PICTURE
        )

        list_albums = list()
        list_artist_tracks = list()

        for dir_album in paths_in_artist:
            album_id = str(uuid.uuid4())
            path_album = os.path.join(DIR_TRACKS, dir_artist, dir_album)

            list_album_tracks = list()

            paths_in_album = os.listdir(path_album)

            if FILE_ALBUM_CHECKED in paths_in_album and SKIP_CHECKED:
                continue
            with open(os.path.join(path_album, FILE_ALBUM_CHECKED), mode='w'):
                pass

            paths_in_album.remove(FILE_ALBUM_INFO)
            paths_in_album.remove(FILE_ALBUM_PICTURE)
            if FILE_ALBUM_CHECKED in paths_in_album:
                paths_in_album.remove(FILE_ALBUM_CHECKED)

            with open(os.path.join(path_album, FILE_ALBUM_INFO), mode='r') \
                    as file_album_info:
                album_info = json.load(file_album_info)
            album_picture_path = os.path.join(path_album, FILE_ALBUM_PICTURE)

            list_albums.append(album_id)

            for file_track in paths_in_album:
                track_id = str(uuid.uuid4())
                path_track = os.path.join(
                    DIR_TRACKS, dir_artist, dir_album, file_track)

                track_name = file_track[4:]
                # print(f'{track_name=}')
                track_name = track_name[:track_name.rfind('.')]
                tags = TinyTag.get(path_track)

                list_artist_tracks.append(track_id)
                list_album_tracks.append(track_id)

                cursor.execute(
                    f'INSERT INTO tracks VALUES (?, ?, ?, ?, ?)',
                    (track_id, json.dumps([artist_id]), album_id,
                     json.dumps({
                         'name': track_name,
                         'duration': tags.duration
                     }), os.path.join('db', path_track))
                )

            cursor.execute(
                f'INSERT INTO albums VALUES (?, ?, ?, ?, ?)',
                (album_id, json.dumps([artist_id]),
                 json.dumps(album_info), os.path.join('db', album_picture_path),
                 json.dumps(list_album_tracks))
            )
            print(f'Added album={album_info["name"]} '
                  f'[{album_id}] to {[artist_id]}')
            file.write(f'Added album={album_info["name"]} '
                       f'[{album_id}] to {[artist_id]}\n')

        if len(list_artist_tracks) == 0:
            continue

        cursor.execute(
            'SELECT * FROM artists WHERE artist_id=?',
            (artist_id, )
        )
        result = cursor.fetchone()
        if result is None:
            cursor.execute(
                f'INSERT INTO artists VALUES (?, ?, ?, ?, ?, ?)',
                (artist_id,  artist_name, json.dumps(artist_info),
                 artist_picture_path, json.dumps(list_albums),
                 json.dumps(list_artist_tracks))
            )
        else:
            cursor.execute(
                f'UPDATE artists set artist_albums=? where artist_id=?',
                (json.loads(result[3]) + list_albums, artist_id)
            )
            cursor.execute(
                f'UPDATE artists set artist_tracks=? where artist_id=?',
                (json.loads(result[4]) + list_artist_tracks, artist_id)
            )

        # Insert superuser
        cursor.execute(
            'INSERT INTO users '
            '(user_id, user_login, user_password, user_email, user_auth_key, '
            'user_birth, user_country, user_photo, user_artists, '
            'user_playlists, user_subscription, last_track_id) '
            'VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
            (str(uuid.uuid4()), 'drunkbear', 'uednoitr',
             'ivanenkogrig@yandex.ru', str(uuid.uuid4()), '11.12.2001',
             'Russia', b'', '', '', 0, '')
        )
        cursor.execute(
            'INSERT INTO users '
            '(user_id, user_login, user_password, user_email, user_auth_key, '
            'user_birth, user_country, user_photo, user_artists, '
            'user_playlists, user_subscription, last_track_id) '
            'VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
            (str(uuid.uuid4()), 'ulw', '15uvopem',
             '333uv555@gmail.com', str(uuid.uuid4()), '05.01.2001', 'Russia',
             b'', '', '', 0, '')
        )

    conn.commit()
    file.close()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        sys.exit()
