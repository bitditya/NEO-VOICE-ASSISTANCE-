# utils.py
import os
from datetime import datetime
import pyautogui

from config import SCREENSHOT_FOLDER

# Create screenshot directory if it doesn't exist
os.makedirs(SCREENSHOT_FOLDER, exist_ok=True)

def take_screenshot(prefix: str = "screenshot") -> str:
    """
    Takes a screenshot and saves it with a timestamp.
    :param prefix: Name prefix for the screenshot.
    :return: Path to the saved screenshot.
    """
    now = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = os.path.join(SCREENSHOT_FOLDER, f"{prefix}_{now}.png")
    img = pyautogui.screenshot()
    img.save(path)
    return path

def current_time_str() -> str:
    """
    Returns the current time as a formatted string.
    """
    return datetime.now().strftime("%A, %d %B %Y %I:%M %p")
