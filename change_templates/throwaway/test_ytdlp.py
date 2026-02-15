import json
import logging
from yt_dlp import YoutubeDL

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('yt_dlp_test')

def fetch_instagram_meta(url):
    ydl_opts = {
        'skip_download': True, # We just want metadata first
        'quiet': True,
        'no_warnings': True,
        'cookiefile': 'cookies.txt', # Might need cookies, but try without first
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            logger.info(f"Fetching info for: {url}")
            info = ydl.extract_info(url, download=False)
            
            print(json.dumps(info, indent=2,  default=str))
            
            # Extract key details
            title = info.get('title') or info.get('description')
            uploader = info.get('uploader')
            url = info.get('url') # Direct media URL
            thumbnail = info.get('thumbnail')
            
            logger.info(f"Title: {title}")
            logger.info(f"Uploader: {uploader}")
            logger.info(f"Media URL: {url}")
            logger.info(f"Thumbnail: {thumbnail}")

    except Exception as e:
        logger.error(f"Error extracting info: {e}")

if __name__ == "__main__":
    target_url = "https://www.instagram.com/p/DIL7ekRoNQw/"
    fetch_instagram_meta(target_url)
