import spotipy
from dotenv import load_dotenv
load_dotenv()
from spotipy.oauth2 import SpotifyOAuth
from config import CLIENT_ID, CLIENT_SECRET, REDIRECT_URI, SCOPE
import os


cache_path="rpi-rgb-led-matrix/bindings/python/LEDproject/.spotipy_cache"

def get_spotify_client():
    oauth = SpotifyOAuth(
        client_id=os.getenv('ID'),
        client_secret=os.getenv('SECRET'),
        redirect_uri=REDIRECT_URI,
        scope=SCOPE,
        cache_path=".spotipy_cache"  # This specifies a file path to store the token information
    )
    
    if not os.path.isfile(".spotipy_cache"):  # Checks if the cache file exists
        auth_url = oauth.get_authorize_url()
        print(f"Please navigate here in your browser: {auth_url}")
        response = input("Enter the URL you were redirected to: ")
        code = oauth.parse_response_code(response)
        token_info = oauth.get_access_token(code)  # Exchanges code for token and caches it
    else:
        token_info = oauth.get_cached_token()  # Retrieves token from cache
    
    if not token_info:
        raise Exception("Authorization failed or token was not cached.")
    
    return spotipy.Spotify(auth=token_info['access_token'])

