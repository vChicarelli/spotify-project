import requests
import os
from dotenv.main import load_dotenv


def songs_playlist(id):
    playlist_url = base_url + "playlists/" + id
    response = requests.get(playlist_url,headers=header)
    playlist_infos = response.json().get('tracks').get('items')
    art_count = {}
    for songs in playlist_infos:
        track = songs.get('track').get('name')
        print(f"Song name - {track}")
        for artist in songs.get('track').get('artists'):
            name = artist.get('name')
            art_count[name] = art_count.get(name) + 1 if name in art_count else 1
         
    top5_names = sorted(art_count.items(), key=lambda item: item[1], reverse=True)
    print(" \nTop 5 artists for this playlist:")
    for x in range(0,5):
        print(f"{x + 1} - {top5_names[x][0]}")
            
def get_playlist():
    url = input("Insira o link da playlist:")
    p_id = url.split("/")[-1].split("?")[0]
    songs_playlist(p_id)


load_dotenv()

CLIENT_ID = os.environ['CLIENT_ID']
CLIENT_SECRET = os.environ['CLIENT_SECRET']
AUTH_URL = "https://accounts.spotify.com/api/token"

base_url = 'https://api.spotify.com/v1/'

auth_response = requests.post(AUTH_URL, {
    'grant_type': 'client_credentials',
    'client_id': CLIENT_ID,
    'client_secret': CLIENT_SECRET,
})

auth_response_data = auth_response.json()

access_token = auth_response_data['access_token']
 
header = {
    'Authorization': 'Bearer {token}'.format(token=access_token)
}


x = -1 
while x != 0:
    print("===== M E N U =====")
    print("1- Verificar playlist")
    print("0- Sair")
    resp = input("Digite uma opção: ")
    if(resp == "1"):
        get_playlist()
    if(resp == "0"):
        exit()