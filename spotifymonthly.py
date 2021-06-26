import spotipy
import os
from spotipy.oauth2 import SpotifyClientCredentials
from collections import defaultdict, Counter

#You gotta set the environment variables "SPOTIPY_CLIENT_ID" and "SPOTIPY_CLIENT_SECRET" with valid Spotify API keys
#os.environ["SPOTIPY_CLIENT_ID"] = 
#os.environ["SPOTIPY_CLIENT_SECRET"] = 
os.environ["SPOTIPY_REDIRECT_URI"] = "http://localhost/"

#prompt for Spotify username and go thru Spotify authentication
username = input("What is your Spotify username?\n")
user_token = spotipy.util.prompt_for_user_token(username, "playlist-modify-public")
sp = spotipy.Spotify(auth=user_token, auth_manager=SpotifyClientCredentials())
auth = spotipy.oauth2.SpotifyPKCE()

#prompt user for desired playlist title text
usr_inp = input("Search for what title string?\n")
query = "name:\"" + usr_inp + "\""

#get up to 50 results from Spotify search using given title query
song_counts = Counter()
results = sp.search(query, 50, type="playlist")
playlists = results["playlists"]["items"]

#for each returned playlist
for playlist in playlists:

    #get list of tracks on playlist by track id
    list_id = playlist["uri"]
    tracks = sp.playlist_tracks(list_id)["items"]
    track_ids = [track["track"]["id"] for track in tracks if track["track"] and track["track"]["id"]] #get the id for each track in the playlist if it is a valid track

    #count each track
    song_counts.update(track_ids)

#get the id of the <=25 most popular tracks in specified playlists, if track occurs in at least 2 playlists
idlist = [id for (id,cnt) in song_counts.most_common(25) if cnt>1]

#make playlist
sp.user_playlist_create(username, "MonthlyMonthly: " + usr_inp) #create new playlist for authenticated user, with title containing given query string
output_playlist = sp.user_playlists(username)["items"][0]["id"] #get playlist id to do other stuff
sp.playlist_add_items(output_playlist, idlist) #add the resulting tracks to new playlist
sp.playlist_change_details(output_playlist, public=False, 
    description="Created using the program Monthly Monthly Playlists by KonoPez on GitHub")#make playlist private and set description