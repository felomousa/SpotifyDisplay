## Config File
from dotenv import load_dotenv
load_dotenv()
from rgbmatrix import RGBMatrixOptions
import os

CLIENT_ID = os.getenv('ID')
CLIENT_SECRET = os.getenv('SECRET')
REDIRECT_URI = 'http://localhost:8888/callback'
SCOPE = 'user-read-currently-playing'
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


progress_bar_config = {
    'bar_pos_x': 35,
    'bar_pos_y': 23,
    'bar_width': 139,
    'bar_height': 2,
}


font_config = {
    'font_path': "PixelOperatorMono8-Bold.ttf",  # Adjust font path as needed
    'font_path1': "PixelOperator.ttf",       # Adjust font path as needed
    'font_size': 8,
    'font_size1': 14,
}