import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth

year=input("The year you wanna travel to (YYYY) :")
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id="CLIENT_ID",
        client_secret="CLIENT_SECRET",
        show_dialog=True,
        cache_path="token.txt"
    )
)
user_id = sp.current_user()["id"]

response=requests.get(f"https://www.billboard.com/charts/year-end/{year}/hot-100-songs/")

soup=BeautifulSoup(response.text,"html.parser")

data=soup.select("div.o-chart-results-list-row-container ul li.lrv-u-width-100p h3#title-of-a-story")
data_2=soup.select("div.o-chart-results-list-row-container ul li.lrv-u-width-100p ul li:first-child span")
songs=[song.getText().replace("\n","").replace("\t","") for song in data]
artists=[artist.getText().replace("\n","").replace("\t","").split("&")[0].split("Featuring")[0] for artist in data_2]

print(artists)

song_uris=[]
for i in range(0,100):
    result = sp.search(q=f"track:{songs[i]} artist:{artists[i]}", type="track")
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{songs[i]} doesn't exist in Spotify. Skipped.")

playlist = sp.user_playlist_create(user=user_id, name=f"Billboard Hottest 100 of {year}", public=False)
playlist_id = playlist['id']

sp.playlist_add_items( playlist_id=playlist_id, items=song_uris)

