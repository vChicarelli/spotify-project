import requests
import os
from dotenv.main import load_dotenv

load_dotenv()

CLIENT_ID = os.environ['CLIENT_ID']
CLIENT_SECRET = os.environ['CLIENT_SECRET']

print(CLIENT_ID)
print(CLIENT_SECRET)

AUTH_URL = "https://accounts.spotify.com/api/token"
auth_response = requests.post(AUTH_URL, {
    'grant_type': 'client_credentials',
    'client_id': CLIENT_ID,
    'client_secret': CLIENT_SECRET,
})

#Convert response to JSON
auth_response_data = auth_response.json()

#Save the access token
access_token = auth_response_data['access_token']
header = {
    'Authorization': 'Bearer {token}'.format(token=access_token)
}

print(header)
base_url = 'https://api.spotify.com/v1/'
playlists_endpoint = 'playlists/79nrN6Y0NwBRjSmCpyxx8M/'
featured_playlists_url = ''.join([base_url,playlists_endpoint])
response = requests.get(featured_playlists_url,params="tracks.items(track(TrackObject(name)))",headers=header)
playlists = response.json().get('tracks').get('items')

for music in playlists:
    song = music.get('track').get('name')
    print(f"Song name {song}")
