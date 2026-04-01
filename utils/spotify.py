import spotipy
from spotipy.oauth2 import SpotifyOAuth

def play_vibe(query, client_id, client_secret, redirect_uri): # 第一引数を query に変更
    scope = "user-modify-playback-state user-read-playback-state"

    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=client_id,
        client_secret=client_secret, 
        redirect_uri=redirect_uri,
        scope=scope
    ))

    try:
        results = sp.search(q=query, type='playlist', limit=1)
        
        if results['playlists']['items']:
            playlist = results['playlists']['items'][0]
            playlist_id = playlist['id']
            playlist_name = playlist['name']
            
            sp.start_playback(context_uri=f"spotify:playlist:{playlist_id}")
            print(f"🎵 Spotify Search Success: '{query}'")
            print(f"▶️ Playing Playlist: {playlist_name} ({playlist_id})")
        else:
            print(f"⚠️ No playlist found for query: {query}")

    except Exception as e:
        print(f"Spotify play errpr: {e}")
        print("ヒント: Spotifyアプリをどこかのデバイスで開いておいてください。")