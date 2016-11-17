from reddit import get_top_20_songs
from spotify import add_songs_to_playlist, get_song_id, create_playlist

from settings import SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI, SPOTIPY_CLIENT_ID

import spotipy
#import spotipy.oauth2 as oauth2
import oauth2

from flask import Flask, request, render_template, redirect, url_for, flash, session, g

app = Flask(__name__)
app.secret_key = 'loPp;j:KJ;kj;KJKkK&&Nhjk!'


@app.route("/", methods=['GET', 'POST'])
def hello():
    if request.method == 'POST':
        username = request.form['username']
        session['username'] = username

        if not SPOTIPY_CLIENT_ID or not SPOTIPY_CLIENT_SECRET or not SPOTIPY_REDIRECT_URI:
            raise spotipy.SpotifyException(550, -1, 'no credentials set')

        sp_oauth = oauth2.SpotifyOAuth(SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI,
                                       scope=None, cache_path=".cache-" + username)

        session['s'] = sp_oauth.serialize()
        print("===s====",session['s'])
        print("===S====", sp_oauth.cache_path)

        token_info = sp_oauth.get_cached_token()

        if not token_info:

            auth_url = sp_oauth.get_authorize_url()

            return redirect(auth_url)

        else:
            return redirect(url_for('songs'))

    return render_template('main.html')


"""
@app.route('/callback')
def callback():
    print("==========CALLBACK===========")
    response = request.url

    code = sp_oauth.parse_response_code(response)
    token_info = sp_oauth.get_access_token(code)
    token = token_info

    #print(token_info)
    return render_template('callback.html', token=token, response=response)
"""

def as_SpotifyOAuth(d):
    return oauth2.SpotifyOAuth(d['client_id'], d['client_secret'], d['redirect_uri'], cache_path=d['cache_path'])

@app.route('/playlist', methods=['GET', 'POST'])
def playlist():
    print("==========PLAYLIST===========")

    code = request.args.get('code')

    sp_oauth = as_SpotifyOAuth(session['s'])
    print("====2====", sp_oauth.cache_path)
    username = session['username']
    # print(username)

    if code:

        token_info = sp_oauth.get_access_token(code)
        print("=====tf====",token_info)
        #sp_oauth._save_token_info(token_info)

        songs = get_top_20_songs()
        return render_template('songs.html', songs=songs, song_id=get_song_id)

    if request.method == 'POST':

        songs = [song for song in request.form.getlist('songs') if song != 'None']

        token_info = sp_oauth.get_cached_token()

        if not token_info:
            flash('Token not cached')
            print('++++++++++++TOKEN NOT CACHED+++++++++++++')

        if token_info:
            token = token_info['access_token']

            sp = spotipy.Spotify(auth=token)
            sp.trace = False
            print("====sp====", sp)

            # create playlist with today's date in the name e.g. "Reddit's /r/Music songs of 2016-11-15"
            playlist_id = create_playlist(sp, username)  # returns playlist id

            # insert list of songs in playlist
            print("SONGS---------------------", songs)
            add_songs_to_playlist(sp, username, playlist_id, songs)

            # success or error

            return render_template('playlist.html', user=username, playlist_id=playlist_id)
        else:
            flash("Token error.")
            return render_template('playlist.html', user=username)


@app.route('/songs', methods=['GET', 'POST'])
def songs():
    songs = get_top_20_songs()
    return render_template('songs.html', songs=songs, song_id=get_song_id)



if __name__ == "__main__":
    app.run()

    # testing : 11158057035
