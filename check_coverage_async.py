import json
from urllib.parse import quote as encodeUri
import asyncio
import aiohttp


async def fetch(session, url, headers):
    async with session.get(url, headers=headers) as response:
        return response


async def search(artists_tracks, token):
    api_search_url = "https://api.spotify.com/v1/search?type=track&limit=1&q="
    headers = {"Authorization": "Bearer " + token}
    urls = []

    for artist_track in artists_tracks:
        search_query = encodeUri(f"{artist_track[0]} {artist_track[1]}")
        url = api_search_url + search_query
        urls.append(url)

    # it seems that spotify api limits the number of simultaneous requests to just 1
    # but feel free to play with the limit (FYI: 429 means "too many requests")
    connector = aiohttp.TCPConnector(limit=1)
    tasks = []
    async with aiohttp.ClientSession(connector=connector) as session:
        for url in urls:
            tasks.append(fetch(session, url, headers))

        responses = await asyncio.gather(*tasks)

        response_codes = {}
        for response in responses:
            code = response.status
            response_codes[code] = response_codes.get(code, 0) + 1

        print(response_codes)

    return response_codes.get(200, 0)


if __name__ == '__main__':
    print("Go here: https://developer.spotify.com/console/get-search-item/ and grab a token (no additional scopes required).")
    token = input("Input Spotify API token: ")

    filename = "maestro-v3.0.0.json"
    with open(filename) as f:
        data = json.load(f)
        artists = data["canonical_composer"]
        tracks = data["canonical_title"]

    artists_tracks = zip(artists.values(), tracks.values())

    loop = asyncio.get_event_loop()
    found_tracks = loop.run_until_complete(search(artists_tracks, token))
    total_tracks = len(tracks)
    print(
        f"Coverage (% of songs from the dataset on Spotify): {100 * found_tracks / total_tracks}%")
