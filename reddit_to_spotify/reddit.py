import praw


def get_top_songs_week(song_num):
    """
    Scrapes Reddit's r/Music
    :param song_num: int, number of songs it needs to return
    :return: generator, containing top 20 posts of last week with the "music streaming" flair
    """
    r = praw.Reddit(user_agent='r_to_s')

    songs = r.search(query="flair:'music streaming'", subreddit="Music", sort="top", period="week", limit=song_num)

    return songs
