import time
import subprocess
from spotipy import oauth2
import spotipy



def create_playlist(spotify_instance, username):
    """
    :param username: string, Spotify username
    :param spotify_instance: object, instance of spotipy.Spotify()
    :return: playlist id OR False if it fails
    """

    if spotify_instance:
        playlist_name = "Reddit's /r/Music songs of {}".format(time.strftime('%Y-%m-%d %H:%M:%S'))

        print("Creating playlist '{}'...".format(playlist_name))

        playlist = spotify_instance.user_playlist_create(username, playlist_name, public=True)

        return playlist['id']

    else:
        print("Error creating the playlist")

        return False


def add_songs_to_playlist(spotify_instance, username, playlist_id, track_ids):
    """
    :param spotify_instance: object, instance of spotipy.Spotify()
    :param username: string, Spotify username
    :param playlist_id: string, alpha-digits id
    :param track_ids: list, contains strings --> all of the tracks' id's
    :return: True if succes, False if error
    """

    if spotify_instance:
        print("Adding songs to playlist...")

        spotify_instance.user_playlist_add_tracks(username, playlist_id, track_ids)

        return True

    else:
        print("Error adding songs to playlist")

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
