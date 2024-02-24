# LedPanel: Spotify LED Panel Display

Welcome to the Spotify LED Panel Display project! This repository hosts a Python application designed to display the currently playing track information from Spotify on an LED panel. The application showcases the song name, artist, album cover, and a progress bar representing the song's playback progress.

## Features
- 🎵 Display of the current playing song's name and artist on an LED panel.
- 🖼️ Dynamic updating of the song's album cover image.
- 📊 A progress bar that visually represents the song's playback state.
- 🔑 Integration with Spotify's Web API to fetch real-time playback information.

## Getting Started
These instructions will guide you through setting up and running the project on your local machine.

### Prerequisites
- A Raspberry Pi or similar device.
- An LED panel compatible with the rgbmatrix library.
- Python 3 installed on your device.
- Installation of the numpy, cv2 (OpenCV), Pillow, requests, and spotipy libraries.
- A Spotify account and an application registered on the Spotify Developer Dashboard to obtain the CLIENT_ID, CLIENT_SECRET, and REDIRECT_URI.

### Installation
1. Clone this repository to your local machine:
```bash
git clone https://github.com/felomousa/LedPanel.git
cd LedPanel
```
2. Install the required Python libraries:
```bash
pip install numpy opencv-python Pillow requests spotipy
```
3. Set up your Spotify application credentials. Edit the `config.py` file to include your CLIENT_ID, CLIENT_SECRET, REDIRECT_URI, and the desired SCOPE for Spotify's API access.

4. Ensure your LED panel is correctly connected to your Raspberry Pi or similar device and that you have configured the options in the `config.py` file according to your panel's specifications.

## Running the Application
To start the application and display the Spotify playback information on your LED panel, run:
```bash
sudo python3 main.py
```
Follow the instructions in the console to authenticate your Spotify account when running the script for the first time.

## Contributing
Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are greatly appreciated.

Please refer to the `CONTRIBUTING.md` file for more information on how to contribute to this project.

## License
This project is licensed under the MIT License - see the `LICENSE.md` file for details.

## Acknowledgments
- Thanks to the creators of the spotipy and rgbmatrix (Using: https://github.com/hzeller/rpi-rgb-led-matrix) libraries for making this project possible.