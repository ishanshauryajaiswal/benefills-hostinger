from playwright.sync_api import sync_playwright
import time

def scrape_instagram_post(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            viewport={'width': 1280, 'height': 800}
        )
        page = context.new_page()

        print(f"Navigating to {url}...")
        try:
            page.goto(url, wait_until="networkidle", timeout=60000)
            
            # Wait a bit for JS hydration if needed
            time.sleep(3)

            # Get Page Title and Meta
            title = page.title()
            print(f"Page Title: {title}")

            # Try to get og:image via JS execution or locator
            og_image = page.locator('meta[property="og:image"]').get_attribute('content')
            og_desc = page.locator('meta[property="og:description"]').get_attribute('content')

            if og_image:
                print(f"Found og:image: {og_image}")
                # Download it
                import requests
                img_data = requests.get(og_image).content
                with open("downloaded_test.jpg", "wb") as f:
                    f.write(img_data)
                print("Downloaded image to downloaded_test.jpg")
            else:
                print("No og:image found via meta tag.")

            if og_desc:
                print(f"Found og:description: {og_desc}")

            # Try to get caption via specific Instagram classes or ARIA labels if needed
            # Often first 'h1' or specific div contains caption text part
            # But let's rely on og:description for now as a fallback

        except Exception as e:
            print(f"Error scraping: {e}")
            page.screenshot(path="error_screenshot.png")
        finally:
            browser.close()

if __name__ == "__main__":
    target_url = "https://www.instagram.com/p/DIL7ekRoNQw/"
    scrape_instagram_post(target_url)
