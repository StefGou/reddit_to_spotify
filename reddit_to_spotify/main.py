from reddit_to_spotify.reddit import get_top_20_songs
from reddit_to_spotify.spotify import add_songs_to_playlist, get_song_id, create_playlist

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

# create playlist with today's date in the name e.g. "Reddit's /r/Music songs of 2016-11-15" -- DONE : create_playlist()
playlist_id = create_playlist(username)
# get playlist id -- DONE : create_playlist returns the id

# get top 20 songs on Reddit/r/Music -- DONE : get_top_20_songs()

# get all songs' id -- DONE : get_song_id()

# put id's into a list
songs = []
for song in get_top_20_songs():
    song_id = get_song_id(song)
    if song_id is not None:
        songs.append(song_id)

# insert list of songs in playlist -- DONE : add_songs_to_playlist()
# print(songs)
add_songs_to_playlist(username, playlist_id, songs)

# success or error
