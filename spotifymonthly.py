import spotipy
import os
from spotipy.oauth2 import SpotifyClientCredentials
from collections import defaultdict, Counter

#You gotta set the environment variables "SPOTIPY_CLIENT_ID" and "SPOTIPY_CLIENT_SECRET" with valid Spotify API keys
#os.environ["SPOTIPY_CLIENT_ID"] = 
#os.environ["SPOTIPY_CLIENT_SECRET"] = 
os.environ["SPOTIPY_REDIRECT_URI"] = "http://localhost/"

username = input("What is your username")
user_token = spotipy.util.prompt_for_user_token(username, "playlist-modify-public")
sp = spotipy.Spotify(auth=user_token, auth_manager=SpotifyClientCredentials())
auth = spotipy.oauth2.SpotifyPKCE()

usr_inp = input("What title string tho")
query = "name:\"" + usr_inp + "\""
song_counts = Counter()

results = sp.search(query, 50, type="playlist")
playlists = results["playlists"]["items"]

#TODO: try playlist_tracks method
for playlist in playlists:

    list_id = playlist["uri"]
    tracks = sp.playlist(list_id)["tracks"]["items"]

    for track in tracks:
        if track["track"] and track["track"]["id"]:
            song_counts.update([track["track"]["id"]])

idlist = [id for (id,cnt) in song_counts.most_common(25) if cnt>1]

sp.user_playlist_create(username, "MonthlyMonthly: " + usr_inp)
output_playlist = sp.user_playlists(username)["items"][0]["id"]
sp.playlist_add_items(output_playlist, idlist)
sp.playlist_change_details(output_playlist, public=False, description="Created using the program Monthly Monthly Playlists by KonoPez on")