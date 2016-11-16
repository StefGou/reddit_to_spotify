import praw


def get_top_20_songs():
    """
    :return: generator, containing top 20 posts of last week with the "music streaming" flair
    """
    print("Searching songs on '/r/Music'...")
    r = praw.Reddit(user_agent='r_to_s')

    songs = r.search(query="flair:'music streaming'", subreddit="Music", sort="top", period="week", limit=20)

    return songs
