import requests
from bs4 import BeautifulSoup

def get_og_image(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
    }
    
    try:
        response = requests.get(url, headers=headers, allow_redirects=True)
        print(f"Status Code: {response.status_code}")
        
        soup = BeautifulSoup(response.text, 'html.parser')
        og_image = soup.find("meta", property="og:image")
        og_desc = soup.find("meta", property="og:description")
        
        if og_image:
            print(f"Found og:image: {og_image['content']}")
        else:
            print("No og:image found.")
            
        if og_desc:
            print(f"Found og:description: {og_desc['content']}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    url = "https://www.instagram.com/p/DIL7ekRoNQw/"
    get_og_image(url)
