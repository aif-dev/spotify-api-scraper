import sys
import json
from urllib.parse import quote as encodeUri
import requests


def save_track_audio_features(dataset_id, tracks_audio_features, response_json):
    try:
        tracks_audio_features[dataset_id] = {
            "danceability": response_json["danceability"],
            "energy": response_json["energy"],
            "key": response_json["key"],
            "loudness": response_json["loudness"],
            "mode": response_json["mode"],
            "speechiness": response_json["speechiness"],
            "acousticness": response_json["acousticness"],
            "instrumentalness": response_json["instrumentalness"],
            "liveness": response_json["liveness"],
            "valence": response_json["valence"],
            "tempo": response_json["tempo"],
            "duration_ms": response_json["duration_ms"],
            "time_signature": response_json["time_signature"]
        }
    except BaseException:
        pass

    print(f"{dataset_id} ({spotify_id}) ::: {tracks_audio_features.get(dataset_id, {})}")


if len(sys.argv) == 2:
    token = sys.argv[1]
else:
    print("Go here: https://developer.spotify.com/console/get-search-item/ and grab a token (no additional scopes required).")
    token = input("Input Spotify API token: ")

api_audio_features_url = "https://api.spotify.com/v1/audio-features/"
headers = {"Authorization": "Bearer " + token}

filename = "data/tracks-with-spotify-ids.json"
with open(filename) as f_in:
    track_ids = json.load(f_in)

tracks_audio_features = {}
for dataset_id in track_ids:
    spotify_id = track_ids.get(dataset_id, "")

    if spotify_id != "":
        url = api_audio_features_url + spotify_id
        response = requests.get(url, headers=headers)
        try:
            response_json = response.json()
            save_track_audio_features(
                dataset_id, tracks_audio_features, response_json)
        except BaseException:
            print(
                f"AN ERROR HAS OCCURED. RESPONSE CODE: {response.status_code}")
    else:
        tracks_audio_features[dataset_id] = {}

filename = "data/tracks-with-audio-features.json"
with open(filename, "w") as f_out:
    f_out.write(json.dumps(tracks_audio_features))
