"""
Instagram scraper module.
Fetches images and captions from public Instagram posts using instaloader.
Falls back gracefully if scraping fails (e.g., private account, rate limit).
"""

import os
import shutil
import tempfile
from abc import ABC, abstractmethod
from typing import List, Dict, Optional

from .logger import setup_logger

logger = setup_logger('scraper')


class ScrapedPost:
    """Represents a scraped Instagram post."""
    def __init__(self, image_path: str, caption: str = "", source_url: str = "",
                 likes: int = 0, comments: int = 0):
        self.image_path = image_path
        self.caption = caption
        self.source_url = source_url
        self.likes = likes
        self.comments = comments

    def to_dict(self) -> dict:
        return {
            "image_path": self.image_path,
            "caption": self.caption,
            "source_url": self.source_url,
            "likes": self.likes,
            "comments": self.comments
        }


class BaseScraper(ABC):
    """Abstract scraper — makes it easy to swap scraping backends or add video later."""

    @abstractmethod
    def scrape_posts(self, urls: List[str], output_dir: str) -> List[ScrapedPost]:
        pass

    @abstractmethod
    def load_local_images(self, image_paths: List[str], output_dir: str) -> List[ScrapedPost]:
        pass


class InstaLoaderScraper(BaseScraper):
    """Scrapes public Instagram posts using instaloader."""

    def scrape_posts(self, urls: List[str], output_dir: str) -> List[ScrapedPost]:
        try:
            import instaloader
        except ImportError:
            logger.error("instaloader not installed. Run: pip install instaloader")
            raise

        loader = instaloader.Instaloader(
            download_videos=False,  # Images only for now
            download_video_thumbnails=False,
            download_geotags=False,
            download_comments=False,
            save_metadata=False,
            compress_json=False,
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        )

        scraped = []
        os.makedirs(output_dir, exist_ok=True)

        for i, url in enumerate(urls):
            try:
                logger.info(f"Scraping post {i+1}/{len(urls)}: {url}")

                # Extract shortcode from URL
                shortcode = self._extract_shortcode(url)
                if not shortcode:
                    logger.warning(f"Could not extract shortcode from: {url}")
                    continue

                # Download to a temp directory then move what we need
                with tempfile.TemporaryDirectory() as tmp_dir:
                    post = instaloader.Post.from_shortcode(loader.context, shortcode)

                    # Download just the image
                    loader.download_post(post, target=tmp_dir)

                    # Find the downloaded image
                    img_file = None
                    for f in os.listdir(tmp_dir):
                        if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
                            img_file = f
                            break

                    if img_file:
                        dest_path = os.path.join(output_dir, f"inspo_{i+1}.jpg")
                        shutil.copy2(os.path.join(tmp_dir, img_file), dest_path)

                        scraped.append(ScrapedPost(
                            image_path=dest_path,
                            caption=post.caption or "",
                            source_url=url,
                            likes=post.likes,
                            comments=post.comments
                        ))
                        logger.info(f"  ✓ Scraped successfully ({post.likes} likes)")
                    else:
                        logger.warning(f"  ✗ No image found in download for: {url}")

            except Exception as e:
                logger.error(f"  ✗ Failed to scrape {url}: {str(e)}")
                continue

        return scraped

    def load_local_images(self, image_paths: List[str], output_dir: str) -> List[ScrapedPost]:
        """Load local images as ScrapedPost objects (for when user provides images directly)."""
        scraped = []
        os.makedirs(output_dir, exist_ok=True)

        for i, path in enumerate(image_paths):
            if os.path.isfile(path):
                dest_path = os.path.join(output_dir, f"inspo_{i+1}{os.path.splitext(path)[1]}")
                shutil.copy2(path, dest_path)
                scraped.append(ScrapedPost(
                    image_path=dest_path,
                    caption="[Local image — no caption available]",
                    source_url=f"file://{os.path.abspath(path)}"
                ))
                logger.info(f"Loaded local image: {path}")
            else:
                logger.warning(f"Image not found: {path}")

        return scraped

    @staticmethod
    def _extract_shortcode(url: str) -> Optional[str]:
        """Extract Instagram shortcode from various URL formats."""
        import re
        # Matches: /p/SHORTCODE/ or /reel/SHORTCODE/
        match = re.search(r'/(p|reel)/([A-Za-z0-9_-]+)', url)
        return match.group(2) if match else None


class MockScraper(BaseScraper):
    """Mock scraper for testing without hitting Instagram."""

    def scrape_posts(self, urls: List[str], output_dir: str) -> List[ScrapedPost]:
        scraped = []
        os.makedirs(output_dir, exist_ok=True)

        # Try to find a placeholder image
        placeholder_path = os.path.join(os.path.dirname(__file__), '..', 'output', 'test_benefills_gen.png')
        
        for i, url in enumerate(urls):
            if os.path.exists(placeholder_path):
                img_path = os.path.join(output_dir, f"inspo_{i+1}.png")
                import shutil
                shutil.copy(placeholder_path, img_path)
                logger.info(f"[MOCK] Copied placeholder scraper image: {img_path}")
            else:
                img_path = os.path.join(output_dir, f"inspo_{i+1}.txt")
                with open(img_path, 'w') as f:
                    f.write(f"[MOCK IMAGE from {url}]")
                logger.info(f"[MOCK] Created text placeholder: {img_path}")

            scraped.append(ScrapedPost(
                image_path=img_path,
                caption=f"Mock caption for post {i+1}: Amazing healthy snack that changed my life! 🌿 #health #wellness",
                source_url=url,
                likes=1500,
                comments=89
            ))
            logger.info(f"[MOCK] Scraped post {i+1}: {url}")

        return scraped

    def load_local_images(self, image_paths: List[str], output_dir: str) -> List[ScrapedPost]:
        return [
            ScrapedPost(
                image_path=p,
                caption="[Mock local image]",
                source_url=f"file://{p}"
            ) for p in image_paths if os.path.exists(p)
        ]



class PlaywrightScraper(BaseScraper):
    """Scrapes public Instagram posts using Playwright (Simulates real browser)."""

    def scrape_posts(self, urls: List[str], output_dir: str) -> List[ScrapedPost]:
        try:
            from playwright.sync_api import sync_playwright
        except ImportError:
            logger.error("playwright not installed. Run: pip install playwright && playwright install chromium")
            raise

        scraped = []
        os.makedirs(output_dir, exist_ok=True)

        with sync_playwright() as p:
            # Launch browser
            try:
                browser = p.chromium.launch(headless=True)
            except Exception as e:
                logger.error(f"Failed to launch browser: {e}. Ensure 'playwright install chromium' is run.")
                raise e

            context = browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
                viewport={'width': 1280, 'height': 800}
            )

            for i, url in enumerate(urls):
                try:
                    logger.info(f"Scraping post {i+1}/{len(urls)}: {url}")
                    page = context.new_page()
                    
                    # Go to URL with timeout
                    page.goto(url, wait_until="networkidle", timeout=60000)
                    
                    # Extract Data
                    og_image = page.locator('meta[property="og:image"]').get_attribute('content')
                    og_desc = page.locator('meta[property="og:description"]').get_attribute('content')

                    if og_image:
                        # Download Image
                        import requests
                        img_data = requests.get(og_image).content
                        dest_path = os.path.join(output_dir, f"inspo_{i+1}.jpg")
                        with open(dest_path, "wb") as f:
                            f.write(img_data)
                        
                        caption = og_desc if og_desc else ""
                        
                        logger.info(f"  ✓ Scraped successfully")
                        scraped.append(ScrapedPost(
                            image_path=dest_path,
                            caption=caption,
                            source_url=url
                        ))
                    else:
                        logger.warning(f"  ✗ No og:image found for: {url}")
                        # Take error screenshot for debug if needed
                        # page.screenshot(path=os.path.join(output_dir, f"error_{i+1}.png"))

                    page.close()

                except Exception as e:
                    logger.error(f"  ✗ Failed to scrape {url}: {str(e)}")
                    continue

            browser.close()

        return scraped

    def load_local_images(self, image_paths: List[str], output_dir: str) -> List[ScrapedPost]:
        """Load local images as ScrapedPost objects."""
        scraped = []
        os.makedirs(output_dir, exist_ok=True)

        for i, path in enumerate(image_paths):
            if os.path.isfile(path):
                dest_path = os.path.join(output_dir, f"inspo_{i+1}{os.path.splitext(path)[1]}")
                shutil.copy2(path, dest_path)
                scraped.append(ScrapedPost(
                    image_path=dest_path,
                    caption="[Local image — no caption available]",
                    source_url=f"file://{os.path.abspath(path)}"
                ))
                logger.info(f"Loaded local image: {path}")
            else:
                logger.warning(f"Image not found: {path}")

        return scraped


class ScraperFactory:
    @staticmethod
    def get_scraper(mock: bool = False) -> BaseScraper:
        if mock:
            return MockScraper()
        return PlaywrightScraper()
