import requests
import os
from dotenv.main import load_dotenv

class Utils:

    def __init__(self):
        load_dotenv()

        CLIENT_ID = os.environ['CLIENT_ID']
        CLIENT_SECRET = os.environ['CLIENT_SECRET']
        AUTH_URL = "https://accounts.spotify.com/api/token"

        self.base_url = 'https://api.spotify.com/v1/'

        auth_response = requests.post(AUTH_URL, {
            'grant_type': 'client_credentials',
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
        })

        auth_response_data = auth_response.json()

        access_token = auth_response_data['access_token']
        
        self.header = {'Authorization': 'Bearer {token}'.format(token=access_token)}
        self.playlist_id = ""
    
    
    def testing():
        print("testing")

    def songs_playlist(self,id):
        playlist_url = self.base_url + "playlists/" + id
        response = requests.get(playlist_url,headers=self.header)
        print(response.json())
        playlist_infos = response.json().get('tracks').get('items')
        user = response.json().get('owner').get('display_name')
        follow_count = response.json().get('followers').get('total')
        total_songs = response.json().get('tracks').get('total')
        art_count = {}
        playlist_songs = []
        for songs in playlist_infos:
            playlist_songs.append(songs.get('track').get('name'))
            for artist in songs.get('track').get('artists'):
                name = artist.get('name')
                art_count[name] = art_count.get(name) + 1 if name in art_count else 1
        top5_names = sorted(art_count.items(), key=lambda item: item[1], reverse=True)
        print(f"\n\nDisplaying playlist created by {user}")
        print(f"Total songs in playlist - {total_songs} and total of {follow_count} followers")
        print(" \nTop 5 artists for this playlist:")
        for x in range(0,5):
            print(f"{x + 1} - {top5_names[x][0]} - appears {top5_names[x][1]} times on this playlist")
        
        self.playlist_id = id if input("Deseja selecionar essa playlist? (S/N):").capitalize() == "S" else ""

    def search_song(self):
        query = input("Search: ")
        query_url = f"{self.base_url}search"
        params = {'q': query, 'type': "track", 'limit': 3}
        
        response = requests.get(query_url, params=params, headers=self.header)

        if response.status_code != 200:
            print("Erro na busca.")
            return
        
        data = response.json()
        tracks = data.get('tracks', {}).get('items', [])
        
        if not tracks:
            print("Nenhuma música encontrada.")
            return
        
        all_results = [{'track': track['name'],
                        'artist': track['artists'][0]['name'],
                        'album': track['album']['name'],
                        'uri': track['uri']} for track in tracks]
        
        for idx, result in enumerate(all_results, start=1):
            print(f"{idx}: {result['track']} - {result['artist']} // {result['album']}")
        
        while True:
            try:
                number = int(input("Escolha uma música (digite o número):"))
                if 1 <= number <= len(all_results):
                    break
                else:
                    print("Número inválido. Tente novamente.")
            except ValueError:
                print("Entrada inválida. Digite um número válido.")

        chosen_song = all_results[number - 1]
        print(f"Escolhida: {chosen_song['track']} - {chosen_song['artist']} // {chosen_song['album']}")
        pick_uri = chosen_song['uri']