from reddit import get_top_20_songs
from spotify import add_songs_to_playlist, get_song_id, create_playlist

import spotipy
import spotipy.util as util

from settings import SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI, SPOTIPY_CLIENT_ID

# get Spotify username
#   username = "11158057035"  # for testing
print("What is your Spotify username?")
print("############################################################################################################")
print("# To find your username, go to https://play.spotify.com/collection, the page will redirect to another one. #")
print("# Look at the URL, you username is just after the '/user/' part.                                           #")
print("# Note that your username can be numbers if you registered via Facebook.                                   #")
print("# e.g. https://play.spotify.com/user/your_user_name_or_numbers/playlist/abc123                             #")
print("############################################################################################################")
print()
username = input("Enter your Spotify username: ")
print()

token = util.prompt_for_user_token(username, client_id=SPOTIPY_CLIENT_ID,
                                   client_secret=SPOTIPY_CLIENT_SECRET, redirect_uri=SPOTIPY_REDIRECT_URI)

if token:
    sp = spotipy.Spotify(auth=token)
    sp.trace = False

    # create playlist with today's date in the name e.g. "Reddit's /r/Music songs of 2016-11-15" -- DONE : create_playlist()
    playlist_id = create_playlist(sp, username) #returns playlist id

    songs = []
    for song in get_top_20_songs(): # get top 20 songs on Reddit/r/Music
        song_id = get_song_id(song)
        if song_id is not None:
            songs.append(song_id)

    # insert list of songs in playlist
    add_songs_to_playlist(sp, username, playlist_id, songs)

    # success or error
    print("Playlist created. https://play.spotify.com/user/{}/playlist/{}".format(username, playlist_id))
else:
    print("Token error.")
