import requests
from bs4 import BeautifulSoup
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from pprint import pprint

SPOTIFY_CLIENT_ID = "57ba76a3dcfc4142b3bcaf9d7e23490b"
SPOTIFY_CLIENT_SECRET = "a976a14eddd243bd8a5f1d7ff8e0e4d9"

date_choice = input("What time period would you like to travel to? Please type in the format YYYY-MM-DD:\n")
year = date_choice.split('-')[0]

# 1992-04-20 <span class="chart-element__information__song text--truncate color--primary">Save The Best For Last</span>
music_url_with_date = "https://www.billboard.com/charts/hot-100/"+date_choice
billboards_response = requests.get(music_url_with_date)
music_parsed = BeautifulSoup(billboards_response.text, "html.parser")
song_titles_tags = music_parsed.find_all(name="span", class_="chart-element__information__song text--truncate "
                                                             "color--primary")
song_titles_list = [titles.text for titles in song_titles_tags]

spotify_scope = "playlist-modify-private"

sp = spotipy.Spotify(
        auth_manager=SpotifyOAuth(
        client_id=SPOTIFY_CLIENT_ID,
        client_secret=SPOTIFY_CLIENT_SECRET,
        scope=spotify_scope,
        redirect_uri="http://example.com",
        username="8cjzxg2uhs0pcpbszmiez98ro",
        show_dialog=True,
        cache_path="token.txt"
    )
)
songs_search_details = {}
user_id = sp.current_user()["id"]

song_uris = []
count_unavailable = 0
for title in song_titles_list:
    try:
        response = sp.search(q=f"track: {title} year:{date_choice.split('-')[0]}", type="track", limit="1")
        song_uris.append(response["tracks"]["items"][-1]["uri"])
    except IndexError:
        count_unavailable += 1
        print(f"{count_unavailable}: {title} is not available  ")

create_playlist_response = sp.user_playlist_create(
    name=f"Top 100 Songs from {date_choice}",
    public="false",
    description=f"Playlist of top 100 songs from the week of {date_choice}",
    user=user_id,
)

playlist_id = create_playlist_response["id"]
add_songs_response = sp.playlist_add_items(playlist_id=playlist_id, items=song_uris)
