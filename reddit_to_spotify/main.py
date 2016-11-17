from reddit import get_top_20_songs
from spotify import add_songs_to_playlist, get_song_id, create_playlist
from settings import SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI, SPOTIPY_CLIENT_ID

from flask import Flask, request, render_template, redirect, url_for, flash, session

import requests
import spotipy
import oauth2

app = Flask(__name__)
app.secret_key = 'loPp;j:KJ;kj;KJKkK&&Nhjk!'


@app.route("/", methods=['GET', 'POST'])
def hello():
    if request.method == 'POST':
        username = request.form['username']
        session['username'] = username

        url = 'https://api.spotify.com/v1/users/{}'.format(username)
        response = requests.get(url).json()
        session['user'] = response

        if not SPOTIPY_CLIENT_ID or not SPOTIPY_CLIENT_SECRET or not SPOTIPY_REDIRECT_URI:
            raise spotipy.SpotifyException(550, -1, 'no credentials set')

        sp_oauth = oauth2.SpotifyOAuth(SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI,
                                       scope=None, cache_path=".cache-" + username)

        session['s'] = sp_oauth.serialize()

        token_info = sp_oauth.get_cached_token()

        if not token_info:

            auth_url = sp_oauth.get_authorize_url()

            return redirect(auth_url)

        else:
            return redirect(url_for('songs'))

    return render_template('main.html')


def as_SpotifyOAuth(d):
    return oauth2.SpotifyOAuth(d['client_id'], d['client_secret'], d['redirect_uri'], cache_path=d['cache_path'])


@app.route('/playlist', methods=['GET', 'POST'])
def playlist():
    if request.method == 'POST':
        sp_oauth = as_SpotifyOAuth(session['s'])
        username = session['username']

        songs = [song for song in request.form.getlist('songs') if not song.startswith('None:')]
        exclusions = [song.split('None:')[1] for song in request.form.getlist('songs') if song.startswith('None:')]

        token_info = sp_oauth.get_cached_token()

        if not token_info:
            flash('Token not cached')

        if token_info:
            token = token_info['access_token']

            sp = spotipy.Spotify(auth=token)
            sp.trace = False

            # create playlist with today's date in the name e.g. "Reddit's /r/Music songs of 2016-11-15"
            playlist_id = create_playlist(sp, username)  # returns playlist id

            # insert list of songs in playlist
            add_songs_to_playlist(sp, username, playlist_id, songs)

            # success or error

            return render_template('playlist.html', user=username, playlist_id=playlist_id, exclusions=exclusions)
        else:
            flash("Token error.")
            return render_template('playlist.html', user=username)

    songs = get_top_20_songs()
    return render_template('songs.html', songs=songs, song_id=get_song_id)


@app.route('/songs', methods=['GET', 'POST'])
def songs():
    code = request.args.get('code')

    if code:
        sp_oauth = as_SpotifyOAuth(session['s'])
        sp_oauth.get_access_token(code)

    return render_template('wait.html')


@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('user', None)

    return redirect('/')


if __name__ == "__main__":
    app.run()

    # testing : 11158057035
