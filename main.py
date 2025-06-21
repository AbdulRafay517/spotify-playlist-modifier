import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import os
import json

# Load environment variables from .env
load_dotenv()

CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")
REDIRECT_URI = os.getenv("SPOTIPY_REDIRECT_URI")
SCOPE = 'playlist-read-private'

# Your target playlists and categories
target_playlists = {
    'romantic': 'romantic songs',
    'beats': 'beats (english)',
    'cruise': 'long trip (friends)',
    'desi hits': 'desi rap / punjabi urdu',
    'classic hits': 'classic hits'
}

# Authenticate using SpotifyOAuth
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scope=SCOPE
))

# Get current user's playlists
user_playlists = sp.current_user_playlists()

# Prepare output dictionary
categorized = {value: [] for value in target_playlists.values()}

# Loop and categorize
for playlist in user_playlists['items']:
    playlist_name = playlist['name'].lower().strip()

    if playlist_name in target_playlists:
        category = target_playlists[playlist_name]
        print(f"\n📥 Fetching from playlist: {playlist['name']} -> Category: {category}")

        results = sp.playlist_tracks(playlist['id'])
        tracks = results['items']

        # Continue fetching if multiple pages
        while results['next']:
            results = sp.next(results)
            tracks.extend(results['items'])

        # Extract track details
        for item in tracks:
            track = item['track']
            if track:
                # Safely get the Spotify URL
                spotify_url = ''
                if 'external_urls' in track and 'spotify' in track['external_urls']:
                    spotify_url = track['external_urls']['spotify']
                
                track_info = {
                    'name': track['name'],
                    'artist': track['artists'][0]['name'],
                    'album': track['album']['name'],
                    'id': track['id'],
                    'url': spotify_url
                }
                categorized[category].append(track_info)

# Save as JSON
with open('categorized_playlists.json', 'w', encoding='utf-8') as f:
    json.dump(categorized, f, ensure_ascii=False, indent=4)

print("\n✅ Done. Songs exported to categorized_playlists.json.")
