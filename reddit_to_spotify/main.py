from reddit import get_top_20_songs
from spotify import add_songs_to_playlist, get_song_id, create_playlist

from settings import SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI, SPOTIPY_CLIENT_ID

import spotipy
import spotipy.oauth2 as oauth2

from flask import Flask, request, render_template, redirect, url_for, flash, session, g

app = Flask(__name__)
app.secret_key = 'loPp;j:KJ;kj;KJKkK&&Nhjk!'


@app.route("/", methods=['GET', 'POST'])
def hello():
    if request.method == 'GET':
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


@app.route('/playlist', methods=['GET', 'POST'])
def playlist():
    print("==========PLAYLIST===========")

    if request.method == 'POST':
        username = request.form['username']
        session['username'] = username

        songs = request.form.getlist('songs')

        if not SPOTIPY_CLIENT_ID or not SPOTIPY_CLIENT_SECRET or not SPOTIPY_REDIRECT_URI:
            raise spotipy.SpotifyException(550, -1, 'no credentials set')

        sp_oauth = oauth2.SpotifyOAuth(SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI,
                                       scope=None, cache_path=".cache-" + username)

        token_info = sp_oauth.get_cached_token()

        if not token_info:
            flash('''
                User authentication requires interaction with your
                web browser. Once you enter your credentials and
                give authorization, you will be redirected to
                a url.  Paste that url you were directed to to
                complete the authorization.
            ''')

            auth_url = sp_oauth.get_authorize_url()

            return redirect(auth_url)

    response = request.args.get('code')

    if response:

        code = sp_oauth.parse_response_code(response)
        token_info = sp_oauth.get_access_token(code)

    if token_info:
        token = token_info['access_token']

        sp = spotipy.Spotify(auth=token)
        sp.trace = False

        # create playlist with today's date in the name e.g. "Reddit's /r/Music songs of 2016-11-15"
        playlist_id = create_playlist(sp, username)  # returns playlist id

        # insert list of songs in playlist
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
