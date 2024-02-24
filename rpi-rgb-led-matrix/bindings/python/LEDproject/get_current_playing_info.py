import spotipy

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