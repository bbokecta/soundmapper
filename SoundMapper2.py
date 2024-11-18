import spotipy
import json
import urllib.request
import spotipy.util as util
import pygeohash as pgh
import time

with open("geocode_keys.txt", "r") as geokey_file:
    geo_key = geokey_file.read()

#getting into spotify heheheheh
cred = "spotify_keys.json"
with open(cred, "r") as spotify_key_file:
    api_tokens = json.load(spotify_key_file)

spotify_key_file.close()

client_id = api_tokens['client_id']
client_secret = api_tokens['client_secret']
redirectURI = api_tokens['redirect']
username = api_tokens['username']

scope = 'user-read-private user-read-playback-state user-modify-playback-state playlist-modify-public user-library-read'
token = util.prompt_for_user_token(username, scope, client_id=client_id,
                           client_secret=client_secret,
                           redirect_uri=redirectURI)

sp = spotipy.Spotify(auth=token)


with open("ticketmaster_keys.txt", "r") as key_file:
    ticketmaster_key = key_file.read()

with open("genreIDs.json", "r") as genreID_file:
    genre_list = json.loads(genreID_file.read())

#asking the user to select a genre
unit = "km"
# user_genre = str(input("Enter a genre IN LOWERCASE (choose from Rock, Pop, Electronic, Classical, Rap, or Country):"))


# address1 = input("Enter starting address or postcode:")
# address2 = input("Enter ending address or postcode:")

def get_more_songs(address1, address2, user_genre):

    addresses = [address1, address2]
    genreID = genre_list[user_genre]

    #cleaning up any spaces or commas in the inputted addresses
    new_addresses = [address
                        .replace(",", "")
                        .replace(" ", "+") for address in addresses]


    #getting the geoPoints for the two addresses
    hash_list = []

    for new_address in new_addresses:
        map_url = f"https://geocode.maps.co/search?q={new_address}&api_key={geo_key}"

        map_request = urllib.request.Request(map_url)
        map_response = urllib.request.urlopen(map_request)

        map_data = json.loads(map_response.read())
        lat = map_data[0]['lat']
        lon = map_data[0]['lon']

        hash_list.append(pgh.encode(float(lat), float(lon), precision=5))

    # print(hash_list)

    #making a function to request ticketmaster's API, using the user's geoPoints + selected genre
    def get_all_events(radius):

        events_both_places = {}
        
        for hash in hash_list:
            url = f"https://app.ticketmaster.com/discovery/v2/events.json?size=20&radius={radius}&genreId={genreID}&geoPoint={hash}&classificationName=music&apikey={ticketmaster_key}"

            tm_request = urllib.request.Request(url)
            tm_response = urllib.request.urlopen(tm_request)

        events_both_places.update(json.loads(tm_response.read()))

        # print(events_both_places)
        return events_both_places

    #running the get_all_events function & increasing radius the until there are at least 3 musical events returned to us
    all_events = {}
    radius = 10
    all_events.update(get_all_events(radius))

    while len(all_events) < 3:
        radius *= 4
        time.sleep(5) #trying to get around the 429 Too Many Requests error
        all_events.update(get_all_events(radius))

    #getting the names of each event's musician
    event_names = all_events['_embedded']['events']

    artist_names = [artist['name'] for artist in event_names]
    artist_names_no_repeats = list(dict.fromkeys(artist_names))



    #making a list of songs from each musician in the returned events
    playlist_songs = []

    for artist in artist_names_no_repeats:
        returned_song = sp.search(q=artist, type="track", limit=1)

        if returned_song['tracks']['items'][0]['uri'] not in playlist_songs: #avoiding duplicate songs
            playlist_songs.append(returned_song['tracks']['items'][0]['uri'])

    genre_name = list(genre_list.keys())[list(genre_list.values()).index(genreID)]

    #adding each song to the playlist
    empty_playlist = sp.user_playlist_create(user=username, name=f"{genre_name} journey from {address1.upper()} to {address2.upper()}", public=True, description=f"{genre_name} artists who've played recently anywhere within a {radius} {unit} radius of {address1.upper()} and {address2.upper()}")
    sp.user_playlist_add_tracks(username, empty_playlist['id'], playlist_songs)

    my_playlistID = empty_playlist['id']
    
    return my_playlistID
# webbrowser.open(empty_playlist['external_urls']['spotify'])
  
