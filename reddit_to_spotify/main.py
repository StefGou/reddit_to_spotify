from reddit import get_top_20_songs
from spotify import add_songs_to_playlist, get_song_id, create_playlist

from settings import SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI, SPOTIPY_CLIENT_ID

import spotipy
import spotipy.oauth2 as oauth2

from flask import Flask, request, render_template, redirect, url_for, flash, session

app = Flask(__name__)
app.secret_key = 'loPp;j:KJ;kj;KJKkK&&Nhjk!'


@app.route("/", methods=['POST', 'GET'])
def hello():
    if request.method == 'POST':
        username = request.form['username']

        session['username'] = username

        ''' prompts the user to login if necessary and returns
            the user token suitable for use with the spotipy.Spotify
            constructor

            Parameters:
             - username - the Spotify username
             - scope - the desired scope of the request
             - client_id - the client id of your app
             - client_secret - the client secret of your app
             - redirect_uri - the redirect URI of your app

        '''

        client_id = SPOTIPY_CLIENT_ID
        client_secret = SPOTIPY_CLIENT_SECRET
        redirect_uri = SPOTIPY_REDIRECT_URI

        if not client_id or not client_secret or not redirect_uri:
            raise spotipy.SpotifyException(550, -1, 'no credentials set')

        global sp_oauth
        sp_oauth = oauth2.SpotifyOAuth(client_id, client_secret, redirect_uri,
                                       scope=None, cache_path=".cache-" + username)

        # try to get a valid token for this user, from the cache,
        # if not in the cache, the create a new (this will send
        # the user to a web page where they can authorize this app)

        global token_info
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

        else:
            #print(token_info)
            return redirect(url_for('playlist'))

    return render_template('main.html')


@app.route('/callback')
def callback():
    print("==========CALLBACK===========")
    response = request.url

    code = sp_oauth.parse_response_code(response)
    token_info = sp_oauth.get_access_token(code)

    print(token_info)
    return redirect(url_for('playlist'))


@app.route('/playlist')
def playlist():
    print("==========PLAYLIST===========")
    if token_info:
        token = token_info['access_token']
        username = session['username']

        sp = spotipy.Spotify(auth=token)
        sp.trace = False

        # create playlist with today's date in the name e.g. "Reddit's /r/Music songs of 2016-11-15" -- DONE : create_playlist()
        playlist_id = create_playlist(sp, username)  # returns playlist id

        songs = []
        for song in get_top_20_songs():  # get top 20 songs on Reddit/r/Music
            song_id = get_song_id(song)
            if song_id is not None:
                songs.append(song_id)

        # insert list of songs in playlist
        add_songs_to_playlist(sp, username, playlist_id, songs)

        # success or error
        flash("Playlist created. https://play.spotify.com/user/{}/playlist/{}".format(username, playlist_id))
        return render_template('playlist.html', user=username)
    else:
        flash("Token error.")


if __name__ == "__main__":
    app.run()
