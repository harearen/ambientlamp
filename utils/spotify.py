import spotipy
from spotipy.oauth2 import SpotifyOAuth

def play_vibe(playlist_id, client_id, client_secret, redirect_uri):
    scope = "user-modify-playback-state user-read-playback-state"

    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=client_id,
        client_secret=client_secret, 
        redirect_uri=redirect_uri,
        scope=scope
    ))

    try:

        sp.start_playback(context_uri=f"spotify:playlist:{playlist_id}")
        print(f"🎵 Spotify Playback Started: {playlist_id}")
    except Exception as e:
        print(f"Spotify再生エラー: {e}")
        print("ヒント: Spotifyアプリをどこかのデバイスで開いておいてください。")