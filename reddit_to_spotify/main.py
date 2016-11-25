from reddit import get_top_songs_week
from spotify import add_songs_to_playlist, get_song_id, create_playlist
from settings import SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI, SPOTIPY_CLIENT_ID

from flask import Flask, request, render_template, redirect, url_for, flash, session

import requests
import spotipy
import oauth2

app = Flask(__name__)
app.secret_key = 'loPp;j:KJ;kj;KJKkK&&Nhjk!'
app.debug = True


def as_SpotifyOAuth(d):
    return oauth2.SpotifyOAuth(d['client_id'], d['client_secret'], d['redirect_uri'], cache_path=d['cache_path'],
                               scope=d['scope'])


@app.route("/", methods=['GET', 'POST'])
def home():
    return render_template('main.html')


@app.route("/login", methods=['GET', 'POST'])
def login():
    if not SPOTIPY_CLIENT_ID or not SPOTIPY_CLIENT_SECRET or not SPOTIPY_REDIRECT_URI:
        raise spotipy.SpotifyException(550, -1, 'no credentials set')

    sp_oauth = oauth2.SpotifyOAuth(SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI,
                                   scope='playlist-modify')

    session['s'] = sp_oauth.serialize()

    token_info = sp_oauth.get_cached_token()

    if not token_info:

        auth_url = sp_oauth.get_authorize_url()

        return redirect(auth_url)

    else:
        return redirect(url_for('songs'))


@app.route('/playlist', methods=['GET', 'POST'])
def playlist():
    if request.method == 'POST':
        sp_oauth = as_SpotifyOAuth(session['s'])
        username = session['user']['id']

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

            return render_template('playlist.html', user=username, playlist_id=playlist_id, exclusions=exclusions)

        else:
            flash("Token error.")
            return render_template('playlist.html', user=username)

    return redirect(url_for('songs'))


@app.route('/songs', methods=['GET', 'POST'])
def songs():
    if request.method == 'POST':
        song_num = request.form.get('song_num')

        songs = get_top_songs_week(int(song_num))

        return render_template('songs.html', songs=songs, song_id=get_song_id, song_num=song_num)

    code = request.args.get('code')

    if code:
        sp_oauth = as_SpotifyOAuth(session['s'])

        token = sp_oauth.get_access_token(code)

        access_token = token['access_token']

        sp = spotipy.Spotify(auth=access_token)

        session['user'] = sp.me()

        sp_oauth.cache_path = 'cache/.cache-{}'.format(session['user']['id'])
        session['s']['cache_path'] = 'cache/.cache-{}'.format(session['user']['id'])
        sp_oauth._save_token_info(token)

    return render_template('wait.html')


@app.route('/logout')
def logout():
    if session.get('username'):
        session.pop('username', None)
    if session.get('user'):
        session.pop('user', None)

    return redirect('/')


# to test html and jinga
@app.route('/test')
def test():
    return render_template('test.html')


if __name__ == "__main__":
    app.run(debug=True)

    # testing : 11158057035
