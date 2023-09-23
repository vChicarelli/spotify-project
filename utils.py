import requests
import os
from dotenv.main import load_dotenv
import funcs
import base64

class Utils:

    def __init__(self):
        load_dotenv()

        CLIENT_ID = os.environ['CLIENT_ID']
        CLIENT_SECRET = os.environ['CLIENT_SECRET']
        AUTH_URL = "https://accounts.spotify.com/api/token"

        auth_response = requests.post(AUTH_URL, {
            'grant_type': 'client_credentials',
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
        },)

        auth_response_data = auth_response.json()
        access_token = auth_response_data['access_token']


        self.header = {'Authorization': 'Bearer {token}'.format(token=access_token)}
        self.base_url = 'https://api.spotify.com/v1/'
        self.playlist_id = ""
    
    
    def track_recomend(self,track):
        recommend_url = f"{self.base_url}recommendations"
        fields = {'seed_tracks': track, 'limit': 5 }
        response = requests.get(recommend_url, params=fields,headers=self.header).json()
        data = response.get('tracks')

        #recommended_songs = [{'name': track.get('name'), 'artist': track.get('artists')[0].get('name',''), 'uri': track.get('uri'),} for track in data]
        recommended_songs = {'items': {'name': track.get('name'), 'artist': track.get('artists')[0].get('name', ''), 'uri': track.get('uri')} for track in data}

        return recommended_songs

    def generate_recomend(self):
        num = int(input("A partir de quantas músicas devo gerar a playlist (usaremos elas como base): "))
        music_list = []
        for x in range(1,num + 1):
            pick_song = self.search_song(input(f"Nome da música ({x}): "))
            track_uri = pick_song.get('uri')
            music_list.append(self.track_recomend(track_uri.split(":")[-1]))
            print(music_list)
        for dabliu in music_list:
            print(dabliu.get('items').get('name'))

    def songs_playlist(self,id):
        playlist_url = f"{self.base_url}playlists/{id}"
        response = requests.get(playlist_url,headers=self.header)

        if response.status_code != 200:
            print("Erro na busca.")
            return
        
        playlist_infos = response.json().get('tracks').get('items')
        user = response.json().get('owner').get('display_name')
        follow_count = response.json().get('followers').get('total')
        total_songs = response.json().get('tracks').get('total')
        
        art_count = {}
        playlist_songs = []

        for songs in playlist_infos:
            tracks = songs.get('track',{})
            playlist_songs.append(tracks.get('name',''))
            for artist in tracks.get('artists',[]):
                name = artist.get('name')
                art_count[name] = art_count.get(name, 0) + 1

        top5_names = sorted(art_count.items(), key=lambda item: item[1], reverse=True)[:5]

        print(f"\n\nDisplaying playlist created by {user}")
        print(f"Total songs in playlist - {total_songs} and total of {follow_count} followers")
        print(" \nTop 5 artists for this playlist:")

        for idx, (name, art_count) in enumerate(top5_names,start = 1):
            print(f"{idx} - {name} - appears {art_count} times on this playlist")
        
        self.playlist_id = id if input("Deseja selecionar essa playlist? (S/N):").capitalize() == "S" else ""

    def search_song(self,query):
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
        if input("Deseja selecionar uma música? (S/N): ").capitalize() == "S":
            chosen_song = funcs.get_input("Escolha uma música (digite o número)", all_results)
            print(f"Escolhida: {chosen_song['track']} - {chosen_song['artist']} // {chosen_song['album']}")
            return chosen_song
            #self.track_recomend(chosen_song['uri'].split(":")[-1])
