import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import json

creds = "spotify_keys.json"
with open(creds, "r") as keys:
    api_tokens = json.load(keys)

client_id = api_tokens['client_id']
client_secret = api_tokens['client_secret']

creds_manager = SpotifyClientCredentials(client_id, client_secret)
sp = spotipy.Spotify(client_credentials_manager=creds_manager)


# print(songs)

def get_songs(year):
    track_results = sp.search(q='year:' +year, type="track", limit=50)

    songs = [track['name'] for track in track_results['tracks']['items']]
    return songs