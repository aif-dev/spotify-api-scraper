import sys
import json
from urllib.parse import quote as encodeUri
import requests


def save_track_id(dataset_id, track_ids, response_json):
    try:
        api_artist_name = response_json["tracks"]["items"][0]["artists"][0]["name"]
        api_track_name = response_json["tracks"]["items"][0]["name"]
        spotify_id = response_json["tracks"]["items"][0]["id"]
        track_ids[dataset_id] = spotify_id
        print(f"{artist_name} - {track_name} ::: {api_artist_name} - {api_track_name}")
    except BaseException:
        track_ids[dataset_id] = ""
        print(f"{artist_name} - {track_name} ::: NOT FOUND")


if len(sys.argv) == 2:
    token = sys.argv[1]
else:
    print("Go here: https://developer.spotify.com/console/get-search-item/ and grab a token (no additional scopes required).")
    token = input("Input Spotify API token: ")

api_search_url = "https://api.spotify.com/v1/search?type=track&limit=1&q="
headers = {"Authorization": "Bearer " + token}

filename = "data/maestro-v3.0.0-clean.json"
with open(filename) as f_in:
    data = json.load(f_in)
    artists = data["canonical_composer"]
    tracks = data["canonical_title"]

artists_tracks = zip(artists.values(), tracks.values(), tracks.keys())

track_ids = {}
for artist_track in artists_tracks:
    artist_name = artist_track[0]
    track_name = artist_track[1]
    dataset_id = artist_track[2]
    search_query = encodeUri(f"{artist_name} {track_name}")
    url = api_search_url + search_query
    response = requests.get(url, headers=headers)
    try:
        response_json = response.json()
        save_track_id(dataset_id, track_ids, response_json)
    except BaseException:
        print(f"AN ERROR HAS OCCURED. RESPONSE CODE: {response.status_code}")

filename = "data/tracks-with-spotify-ids.json"
with open(filename, "w") as f_out:
    f_out.write(json.dumps(track_ids))
