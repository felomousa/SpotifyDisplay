import os
import time
import requests
import numpy as np
import cv2
from spotipy.oauth2 import SpotifyOAuth
from PIL import Image, ImageDraw, ImageFont
from rgbmatrix import RGBMatrix
import spotipy

# Import configuration settings for the application, including Spotify and display settings.
from config import options, progress_bar_config, font_config 
from config import CLIENT_ID, CLIENT_SECRET, REDIRECT_URI, SCOPE

# Setup for HTTPS requests
os.environ['REQUESTS_CA_BUNDLE'] = '/etc/ssl/certs/ca-certificates.crt'

# Path to environment cache file
envcache = '/home/pi/LedPanel/rpi-rgb-led-matrix/bindings/python/LEDproject/.env'

# Initialize the RGB Matrix using configuration options
matrix = RGBMatrix(options=options)

def get_spotify_client():
    """Initialize and return a Spotify client using OAuth for user authentication."""
    oauth = SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        scope=SCOPE,
        cache_path=".spotipy_cache"  # Cache file path for token information
    )
    
    # Check for existing cached token, else request new authorization
    if not os.path.isfile(".spotipy_cache"):
        auth_url = oauth.get_authorize_url()
        print(f"Please navigate here in your browser: {auth_url}")
        response = input("Enter the URL you were redirected to: ")
        code = oauth.parse_response_code(response)
        token_info = oauth.get_access_token(code)  # Exchange code for token
    else:
        token_info = oauth.get_cached_token()  # Retrieve token from cache
    
    if not token_info:
        raise Exception("Authorization failed or token was not cached.")
    
    return spotipy.Spotify(auth=token_info['access_token'])

def get_current_playing_info(spotify_client):
    """Fetch and return information about the currently playing track on Spotify."""
    current_track = spotify_client.current_user_playing_track()
    if current_track is None:
        return None, None, None, None, None, None
    song_name = current_track['item']['name']
    album_name = current_track['item']['album']['name']
    artist_name = ", ".join([artist['name'] for artist in current_track['item']['artists']])
    album_cover_url = current_track['item']['album']['images'][0]['url']
    progress_ms = current_track['progress_ms']
    duration_ms = current_track['item']['duration_ms']
    return song_name, album_name, artist_name, album_cover_url, progress_ms, duration_ms

def draw_progress_bar(draw, progress_ratio, pos_x, pos_y, width, height):
    """Draw a progress bar on the display to indicate song playback progress."""
    bar_fill_width = int(width * progress_ratio)
    # Background bar
    draw.rectangle([(pos_x, pos_y), (pos_x + width, pos_y + height)], fill=(50, 50, 50))
    # Filled portion of the bar
    draw.rectangle([(pos_x, pos_y), (pos_x + bar_fill_width, pos_y + height)], fill=(255, 255, 255))

def main():
    spotifyClient = get_spotify_client()
    fontTitle = ImageFont.truetype(font_config['font_path'], font_config['font_size'])
    fontSubtitle = ImageFont.truetype(font_config['font_path1'], font_config['font_size1'])

    # Setup progress bar parameters from configuration
    bar_pos_x = progress_bar_config['bar_pos_x']
    bar_pos_y = progress_bar_config['bar_pos_y']
    bar_width = progress_bar_config['bar_width']
    bar_height = progress_bar_config['bar_height']

    # Initialize variables to track song changes and progress
    last_update_time = time.time()
    last_song_name = None
    last_artist_name = None
    last_album_cover_url = None
    last_progress_ratio = -1  # Ensure progress bar updates on first run

    while True:
        current_time = time.time()
        time_elapsed = current_time - last_update_time

        # Fetch current playing song information
        song_name, album_name, artist_name, album_cover_url, progress_ms, duration_ms = get_current_playing_info(spotifyClient)
        
        # Update the display only if the album cover has changed
        if album_cover_url != last_album_cover_url:
            headers = {'User-Agent': 'Mozilla/5.0'}
            image_response = requests.get(album_cover_url, headers=headers)
            if image_response.status_code == 200:
                try:
                    # Load and process the album cover image
                    image_array = np.asarray(bytearray(image_response.content), dtype=np.uint8)
                    image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
                    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                    pil_image = Image.fromarray(rgb_image)
                    pil_image.thumbnail((options.cols * options.chain_length, options.rows))
                    final_image = Image.new("RGB", (options.cols * options.chain_length, options.rows), (0, 0, 0))
                    final_image.paste(pil_image, (0, 0))
                    last_album_cover_url = album_cover_url
                except Exception as e:
                    print(f"Failed to load or process the image: {e}")
            else:
                print(f"Failed to fetch image. HTTP Status: {image_response.status_code}")

        # Update song name and artist information on the display
        if song_name != last_song_name or artist_name != last_artist_name:
            draw = ImageDraw.Draw(final_image)
            draw.text((34, 1), f"{song_name}", fill=(255, 255, 255), font=fontTitle)
            draw.text((34, 7), f"{artist_name}", fill=(120, 120, 120), font=fontSubtitle)
            last_song_name = song_name
            last_artist_name = artist_name

        # Calculate and draw the progress bar
        progress_ratio = progress_ms / duration_ms
        draw_progress_bar(draw, progress_ratio, bar_pos_x, bar_pos_y, bar_width, bar_height)
        matrix.SetImage(final_image.convert('RGB'))

        # Reset update timer and delay next update
        last_update_time = current_time
        time.sleep(1)  # Adjust as necessary for update frequency

if __name__ == "__main__":
    main()
