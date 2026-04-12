import spotipy
from spotipy.oauth2 import SpotifyOAuth
import time

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
            return False, {"status": "No device"} # 2つの値を返すように統一

        results = sp.search(q=query, type='playlist', limit=1)
        
        if results['playlists']['items']:
            playlist = results['playlists']['items'][0]
            playlist_id = playlist['id']
            playlist_name = playlist['name']
            playlist_uri = playlist['uri']
            album_art = playlist['images'][0]['url'] if playlist['images'] else ""
            
            sp.start_playback(device_id=active_device_id, context_uri=playlist_uri)

            # 再生が反映されるまで少し待機
            time.sleep(1.5)
            current_track = sp.current_user_playing_track()

            # 初期値を設定してエラーを防ぐ
            track_name = "Unknown Track"
            artist_name = "Unknown Artist"

            if current_track and current_track.get('item'):
                track_name = current_track['item']['name']
                artist_name = ", ".join([artist['name'] for artist in current_track['item']['artists']])
                print(f"🎶 Now playing: '{track_name}' by {artist_name} from playlist '{playlist_name}'")

            return True, {
                    "track": track_name,
                    "artist": artist_name,
                    "album_art": album_art,
                    "playlist": playlist_name
                }
        else:
            print(f"⚠️ No playlist found for query: {query}")
            return False, {"status": "No playlist found"} # 2つの値を返すように統一

    except Exception as e:
        print(f"Spotify play error: {e}")
        return False, {"status": "Error", "details": str(e)} # 2つの値を返すように統一

def stop_spotify(client_id, client_secret, redirect_uri):
    # (stop_spotify はそのままでも概ね大丈夫ですが、一応 return を安定させます)
    scope = "user-modify-playback-state user-read-playback-state"
    auth_manager = SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri, scope=scope, cache_path=".spotify_cache", open_browser=False)
    sp = spotipy.Spotify(auth_manager=auth_manager)
    try:
        sp.pause_playback()
        return True
    except Exception as e:
        print(f"Spotify stop error: {e}")
        return False