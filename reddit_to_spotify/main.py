from reddit_to_spotify.reddit import get_top_20_songs
from reddit_to_spotify.spotify import add_songs_to_playlist, get_song_id

username = "11158057035"  # for testing
playlist_id = '5nTJOjNW9WuC9U0TNnsG5x'  # already created playlist for testing

# get Spotify username

# create playlist with today's date as name e.g. "Reddit's /r/Music songs of 16-11-15"

# get playlist id

# get top 20 songs on Reddit/r/Music -- DONE : get_top_20_songs()

# get all songs' id -- DONE : get_song_id()

# put id's into a list
songs = []
for song in get_top_20_songs():
    song_id = get_song_id(song)
    if song_id is not None:
        songs.append(song_id)

# insert list of songs in playlist -- DONE : add_songs_to_playlist()
print(songs)
# add_songs_to_playlist(username, playlist_id, songs)

# success or error
