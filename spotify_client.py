import requests
import urllib.parse


class Song(object):
    def __init__(self, artist, track):
        self.artist = artist
        self.track = track


class ImageFormat(object):
    def __init__(self, name, url, width, height):
        self.name = name
        self.url = url
        self.width = width
        self.height = height


class SpotifyClient(object):
    def __init__(self, api_token):
        self.api_token = api_token

    def browse_categories(self):
        list_of_image_format = []
        url = f"https://api.spotify.com/v1/browse/categories"
        response = requests.get(
            url,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_token}"
            }
        )

        response_json = response.json()
        categories = response_json['categories']['items']

        for item in categories:
            name = item['name']
            url = item['icons'][0]['url']
            height = item['icons'][0]['height']
            width = item['icons'][0]['width']

            list_of_image_format.append(ImageFormat(name, url, width, height))

        return list_of_image_format

    def search_song(self, artist, track):
        query = urllib.parse.quote(f'{artist} {track}')
        url = f'https://api.spotify.com/v1/search?q=track:{track}+artist:{artist}&type=track'
        response = requests.get(
            url,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_token}"
            }
        )

        response_json = response.json()

        print(response_json)

        results = response_json['tracks']['items']

        if results:
            return results[0]['id']
        else:
            Exception(f"No song found for {artist} = {track}")

    def add_song_to_spotify(self, song_id):
        url = "https://api.spotify.com/v1/me/tracks"
        response = requests.put(
            url,
            json={
                'ids': [song_id]
            },
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_token}"
            }
        )

        return response.ok
