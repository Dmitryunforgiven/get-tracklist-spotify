import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import os
import time

load_dotenv()

SPOTIPY_CLIENT_ID = os.getenv('SPOTIPY_CLIENT_ID')
SPOTIPY_CLIENT_SECRET = os.getenv('SPOTIPY_CLIENT_SECRET')
SPOTIPY_REDIRECT_URI = os.getenv('SPOTIPY_REDIRECT_URI')
USERID = os.getenv('USERID')


scope = "user-library-read"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
 
def get_playlist_id(userid):
    results = sp.user_playlists(userid, limit = 50, offset = 0)

    for idx, item in enumerate(results['items']):
        id = item['id']
        playlist_name = item['name']
        print(idx, f"playlist name = {playlist_name},  id = {id}")


def get_song_list(playlist_id):
    offset = 0
    global_idx = 0

    with open("song_list.txt", "a", encoding="utf-8") as file:
        while True:
            results = sp.playlist_items(
                playlist_id='6JXUbQgx3Up9Mpy7IZO3iU',
                fields=None,
                limit=100,
                offset=offset,
                market=None,
                additional_types=('track', 'episode')
            )

            for item in results['items']:
                track = item['track']
                artist_name = track['artists'][0]['name']
                track_name = track['name']
                duration = track['duration_ms']
                time_sec = duration // 1000
                time_min = time_sec // 60
                time_sec = time_sec % 60
                if time_sec < 10:
                    time_sec = f'0{time_sec}'

                line = f'{global_idx}   {artist_name} - {track_name}, {time_min}:{time_sec}\n'
                file.write(line)
                global_idx += 1
                
            if len(results['items']) < 100:
                print('done')
                break
            offset += 100
            print(offset)
            time.sleep(1)


#get_playlist_id(USERID)
get_song_list(playlist_id='6JXUbQgx3Up9Mpy7IZO3iU')