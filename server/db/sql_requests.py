from sqlite3.dbapi2 import Cursor


def create_tables(cursor: Cursor):
    cursor.execute(
        'CREATE TABLE IF NOT EXISTS artists '
        '(artist_id text, artist_name text, artist_info text, '
        'artist_picture_path text, artist_albums text, artist_tracks text)'
    )
    cursor.execute(
        'CREATE TABLE IF NOT EXISTS albums '
        '(album_id text, album_artists_id text, '
        'album_info text, album_picture_path text, album_tracks text)'
    )
    cursor.execute(
        'CREATE TABLE IF NOT EXISTS playlists '
        '(playlist_id text, playlist_authors_id text, '
        'playlist_info text, playlist_picture_path text, '
        'playlist_tracks text)'
    )
    cursor.execute(
        'CREATE TABLE IF NOT EXISTS tracks '
        '(track_id text, track_artists_id text, track_album_id text, '
        'track_info text, track_path text)'
    )
    cursor.execute(
        'CREATE TABLE IF NOT EXISTS users '
        '(user_id text, user_login text, user_password text, user_email text, '
        'user_auth_key text, user_birth text, user_country text, '
        'user_other_data text, user_photo blob, user_artists text, '
        'user_playlists text, user_subscription integer, last_track_id text)'
    )
    cursor.execute(
        'CREATE TABLE IF NOT EXISTS reset_codes '
        '(reset_code text, user_email text, reset_code_time_expire text)'
    )
