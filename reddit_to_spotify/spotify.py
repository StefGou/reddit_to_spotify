import time
import spotipy
import spotipy.util as util
from reddit_to_spotify.settings import SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI, SPOTIPY_CLIENT_ID


def create_playlist(username):
    """
    :param username: string, Spotify username
    :return: playlist id OR False if it fails
    """
    token = util.prompt_for_user_token(username, client_id=SPOTIPY_CLIENT_ID,
                                       client_secret=SPOTIPY_CLIENT_SECRET, redirect_uri=SPOTIPY_REDIRECT_URI)

    if token:
        playlist_name = "Reddit's /r/Music songs of {}".format(time.strftime('%Y-%m-%d'))

        sp = spotipy.Spotify(auth=token)
        sp.trace = False
        playlist = sp.user_playlist_create(username, playlist_name, public=True)

        return playlist['id']

    else:
        print("Can't get token for", username)

        return False


def add_songs_to_playlist(username, playlist_id, track_ids):
    """
    :param username: string, Spotify username
    :param playlist_id: string, alpha-digits id
    :param track_ids: list, contains strings --> all of the tracks' id's
    :return: True if succes, False if error
    """

    scope = 'playlist-modify-public'

    token = util.prompt_for_user_token(username, scope=scope, client_id=SPOTIPY_CLIENT_ID,
                                       client_secret=SPOTIPY_CLIENT_SECRET, redirect_uri=SPOTIPY_REDIRECT_URI)

    if token:
        sp = spotipy.Spotify(auth=token)
        sp.trace = False
        results = sp.user_playlist_add_tracks(username, playlist_id, track_ids)
        print(results)

        return True

    else:
        print("Can't get token for", username)

        return False


def get_song_id(song):
    """
    :param song: string, title of Reddit post. e.g. "The Bealtes - She loves you [rock]"
    :return: string, id of a Spotify song OR None, if song id is not found
    """

    # split at "[" to keeps only band name and song title
    song = song.title.split("[")[0].strip()

    print('Getting Spotify ID for: {}...'.format(song))

    # split the band name and the song title
    song = song.split(" - ")

    spotify = spotipy.Spotify()

    results = spotify.search(q='artist:{} track:{}'.format(song[0], song[1]))

    try:
        song_id = results['tracks']['items'][0]['id']
        return song_id

    except:
        print('*** Song not found. Skipping...')
        return None
