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
            compress_json=False
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

        for i, url in enumerate(urls):
            img_path = os.path.join(output_dir, f"inspo_{i+1}.txt")
            with open(img_path, 'w') as f:
                f.write(f"[MOCK IMAGE from {url}]")

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


class ScraperFactory:
    @staticmethod
    def get_scraper(mock: bool = False) -> BaseScraper:
        if mock:
            return MockScraper()
        return InstaLoaderScraper()
