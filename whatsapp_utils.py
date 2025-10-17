# whatsapp_utils.py
import pywhatkit
import datetime

def send_whatsapp_message(phone: str, message: str, wait_seconds: int = 20):
    """
    Schedules a WhatsApp Web message a few seconds in the future.
    Note: This opens a browser window and requires you to be logged into WhatsApp Web.
    phone: with country code, e.g. +911234567890
    """
    now = datetime.datetime.now() + datetime.timedelta(seconds=wait_seconds)
    hour = now.hour
    minute = now.minute
    # pywhatkit will open the browser and send at the scheduled minute.
    pywhatkit.sendwhatmsg(phone, message, hour, minute)
