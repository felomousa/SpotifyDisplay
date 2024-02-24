import os
import time
import requests
import numpy as np
import cv2
from PIL import Image, ImageOps, ImageDraw, ImageFont
from rgbmatrix import RGBMatrix, RGBMatrixOptions
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import lyricsgenius

os.environ['REQUESTS_CA_BUNDLE'] = '/etc/ssl/certs/ca-certificates.crt'

# Spotify client credentials - replace these with your actual credentials
CLIENT_ID = "38c9c5e542514a2f832f2ecd9fce651b"
CLIENT_SECRET = "789b01e2f5314632965b9910cb6fbb5f"
REDIRECT_URI = 'http://localhost:8888/callback'
SCOPE = 'user-read-currently-playing'
GENIUS_ACCESS_TOKEN = "_n_6LDZPs1VIkyxAFktrAO4TpvFPMc05DXeTvDG0zSBwPMnk5uq9MMe_qMvwYbkP"
options = RGBMatrixOptions()
options.rows = 32
options.cols = 64
options.chain_length = 3
options.hardware_mapping = 'regular'  # Adjust if using Adafruit HAT
options.brightness = 50  # Example: Set brightness to 50%
options.pwm_bits = 11  # Default is 11, but you can reduce if experiencing issues
options.pwm_lsb_nanoseconds = 130  # Increase if you see ghosting
options.led_rgb_sequence = "RGB"  # Adjust if colors are swapped
options.scan_mode = 1  # 0 for progressive, 1 for interlaced. Change if needed.
options.gpio_slowdown = 3

def get_spotify_client():
    oauth = SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
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

def get_current_playing_info(spotify_client):
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
    bar_fill_width = int(width * progress_ratio)
    draw.rectangle([(pos_x, pos_y), (pos_x + width, pos_y + height)], fill=(50, 50, 50))  # Draw the background bar
    draw.rectangle([(pos_x, pos_y), (pos_x + bar_fill_width, pos_y + height)], fill=(255, 255, 255))  # Draw the filled bar


def display_lyrics_on_matrix(song_name, artist_name, lyrics, matrix):
    font_path = "fonts/PixelOperator.ttf"  # Adjust font path as needed
    font = graphics.Font()
    font.LoadFont(font_path)

    # Create a canvas to draw on
    canvas = matrix.CreateFrameCanvas()

    # Draw song name and artist name
    graphics.DrawText(canvas, font, 1, 8, graphics.Color(255, 255, 255), song_name)
    graphics.DrawText(canvas, font, 1, 20, graphics.Color(120, 120, 120), artist_name)

    # Draw progress bar
    progress_ratio = 0.5  # You need to calculate this based on the progress of the song
    draw_progress_bar(canvas, progress_ratio)

    # Display lyrics line by line
    y = 32
    for line in lyrics:
        graphics.DrawText(canvas, font, 1, y, graphics.Color(255, 255, 255), line)
        y += font.height + 2  # Adjust spacing between lines

    # Swap the canvas to display the changes
    matrix.SwapOnVSync(canvas)


def main():
    spotify_client = get_spotify_client()
    matrix = RGBMatrix(options=options)
    font_path = "fonts/PixelOperator8-Bold.ttf"  # Adjust font path as needed
    font_path1 = "fonts/PixelOperator.ttf"  # Adjust font path as needed
    font = ImageFont.truetype(font_path, 8)
    font1 = ImageFont.truetype(font_path1, 14)

    last_update_time = time.time()

    while True:
        current_time = time.time()
        time_elapsed = current_time - last_update_time

        song_name, artist_name, _, _, _, _ = get_current_playing_info(spotify_client)
        if song_name and artist_name:
            # Fetch lyrics
            genius = lyricsgenius.Genius(GENIUS_ACCESS_TOKEN)
            song = genius.search_song(song_name, artist_name)
            if song:
                lyrics = song.lyrics.split('\n')
                display_lyrics_on_matrix(song_name, artist_name, lyrics, matrix)  # Pass the matrix object
            else:
                print("Lyrics not found for the current song.")
        
        last_update_time = current_time
        time.sleep(1)  # Adjust timing as needed

if __name__ == "__main__":
    main()


if __name__ == "__main__":
    main()
