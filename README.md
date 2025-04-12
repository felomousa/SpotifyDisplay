# SpotifyDisplay

Displays real-time Spotify playback data on an LED matrix using a Raspberry Pi.

## Features
- shows current track name and artist
- displays album cover image
- renders a playback progress bar
- pulls data via Spotify Web API

## Requirements
- Raspberry Pi (or equivalent)
- LED matrix compatible with `rgbmatrix` (https://github.com/hzeller/rpi-rgb-led-matrix)
- Python 3
- Libraries: `numpy`, `opencv-python`, `Pillow`, `requests`, `spotipy`
- Spotify Developer account with app credentials (CLIENT_ID, CLIENT_SECRET, REDIRECT_URI)

## Setup

1. clone the repo:
   ```bash
   git clone https://github.com/felomousa/LedPanel.git
   cd LedPanel
   ```

2. install dependencies:
   ```bash
   pip install numpy opencv-python Pillow requests spotipy
   ```

3. edit `config.py` with your Spotify app credentials and panel configuration.

4. connect and configure your LED matrix hardware.

## Run

```bash
sudo python3 main.py
```

on first run, follow the console instructions to authenticate with Spotify.

![spotify_demo2](https://github.com/user-attachments/assets/32a335f9-60d5-4535-b791-1165be4f706a)

## Relevant Skills
- API integration (Spotify Web API)

- Real-time data processing

- Image handling + display (OpenCV, Pillow)

- Raspberry Pi & GPIO

- Linux service scheduling

## License

MIT — see `LICENSE.md`.

## Credits

uses:
- [spotipy](https://github.com/plamere/spotipy)
- [rpi-rgb-led-matrix](https://github.com/hzeller/rpi-rgb-led-matrix)
