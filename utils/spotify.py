import spotipy
from spotipy.oauth2 import SpotifyOAuth

def play_vibe(query, client_id, client_secret, redirect_uri): 
    scope = "user-modify-playback-state user-read-playback-state"

    auth_manager = SpotifyOAuth(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri,
        scope=scope,
        cache_path=".spotify_cache",
        open_browser=False)

    sp = spotipy.Spotify(auth_manager=auth_manager)

    try:
        devices = sp.devices()
        active_device_id = None

        for d in devices.get('devices', []):
            if d.get('is_active'):
                active_device_id = d['id']
                break

        if not active_device_id and devices.get('devices'):
            active_device_id = devices['devices'][0]['id']
            print(f"⚠️ No active device found. Defaulting to: {devices['devices'][0]['name']}")
        
        if not active_device_id:
            print("⚠️ No Spotify devices available. Please open Spotify on a device and try again.")
            return False 

        
        results = sp.search(q=query, type='playlist', limit=1)
        
        if results['playlists']['items']:
            playlist = results['playlists']['items'][0]
            playlist_id = playlist['id']
            playlist_name = playlist['name']
            playlist_uri = playlist['uri']
            
            sp.start_playback(device_id=active_device_id, context_uri=playlist_uri)
            return True  
        else:
            print(f"⚠️ No playlist found for query: {query}")
            return False 

    except Exception as e:
        print(f"Spotify play errpr: {e}")
        print("Quick tip: Make sure you've got Spotify running on your phone or PC!")