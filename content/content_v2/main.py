#!/usr/bin/env python3
"""
Content Workflow V2 — Instagram Image Post Generator
=====================================================
Generates brand-specific Instagram image posts for Benefills,
inspired by competitor content.

Usage:
    # From Instagram links
    python main.py --links "https://instagram.com/p/ABC123"

    # From local images
    python main.py --images path/to/inspo1.jpg path/to/inspo2.png

    # Mock mode (no API calls)
    python main.py --links "https://instagram.com/p/ABC123" --mock

    # From a file of links
    python main.py --links-file input/links.txt
"""

import argparse
import json
import os
import sys
from datetime import datetime

# Ensure the project root is on the path
sys.path.insert(0, os.path.dirname(__file__))

from modules.scraper import ScraperFactory
from modules.analyzer import AnalyzerFactory
from modules.caption_gen import CaptionGeneratorFactory
from modules.image_gen import ImageGeneratorFactory, build_image_prompt
from modules.reviewer import ReviewerFactory
from modules.logger import setup_logger, RunLogger
from modules.utils import load_brand_context, validate_instagram_url, validate_image_file


logger = setup_logger('pipeline', os.path.join(os.path.dirname(__file__), 'output'))


def parse_args():
    parser = argparse.ArgumentParser(
        description="Benefills Content Workflow V2 — Instagram Image Post Generator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py --links "https://instagram.com/p/ABC123" --style lifestyle
  python main.py --images inspo1.jpg inspo2.png --variants 3
  python main.py --links-file input/links.txt --mock
        """
    )

    # Input sources (at least one required)
    input_group = parser.add_argument_group('Input (provide at least one)')
    input_group.add_argument("--links", nargs="+", type=str,
                             help="Instagram post URLs for inspiration")
    input_group.add_argument("--links-file", type=str,
                             help="Path to a text file with one Instagram URL per line")
    input_group.add_argument("--images", nargs="+", type=str,
                             help="Paths to local inspiration images")
    input_group.add_argument("--topic", type=str,
                             help="Topic/Theme for generating content from scratch (no inspiration needed)")

    # Generation options
    gen_group = parser.add_argument_group('Generation Options')
    gen_group.add_argument("--style", type=str,
                           choices=["poster", "flatlay", "lifestyle", "editorial", "amazon"],
                           default="lifestyle",
                           help="Image generation style (default: lifestyle)")
    gen_group.add_argument("--variants", type=int, default=2,
                           help="Number of caption/image variants to generate (default: 2)")
    gen_group.add_argument("--image-provider", type=str,
                           choices=["google", "dalle"],
                           default="google",
                           help="Image generation provider (default: google)")
    gen_group.add_argument("--text-provider", type=str,
                           choices=["claude", "gemini"],
                           default="claude",
                           help="Text/analysis provider (default: claude)")

    # Workflow flags
    flow_group = parser.add_argument_group('Workflow Flags')
    flow_group.add_argument("--mock", action="store_true",
                            help="Run in mock mode (no API calls)")
    flow_group.add_argument("--skip-scrape", action="store_true",
                            help="Skip scraping — use images already in input/")
    flow_group.add_argument("--skip-images", action="store_true",
                            help="Skip image generation — only produce captions")
    flow_group.add_argument("--skip-review", action="store_true",
                            help="Skip AI quality review step")

    return parser.parse_args()


def collect_inputs(args) -> dict:
    """Collect and validate all input sources."""
    links = []
    images = []

    if args.links:
        for url in args.links:
            if validate_instagram_url(url):
                links.append(url)
            else:
                logger.warning(f"Invalid Instagram URL (skipping): {url}")

    if args.links_file:
        if os.path.isfile(args.links_file):
            with open(args.links_file, 'r') as f:
                for line in f:
                    url = line.strip()
                    if url and validate_instagram_url(url):
                        links.append(url)
                    elif url:
                        logger.warning(f"Invalid URL in file (skipping): {url}")
        else:
            logger.error(f"Links file not found: {args.links_file}")

    if args.images:
        for path in args.images:
            if validate_image_file(path):
                images.append(path)
            else:
                logger.warning(f"Invalid image file (skipping): {path}")

    if not links and not images and not args.topic:
        logger.error("No valid inputs provided. Use --links, --links-file, --images, or --topic.")
        sys.exit(1)

    return {"links": links, "images": images, "topic": args.topic}


def main():
    args = parse_args()

    # Setup run output directory
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    project_root = os.path.dirname(__file__)
    run_dir = os.path.join(project_root, "output", f"run_{timestamp}")
    os.makedirs(run_dir, exist_ok=True)

    run_log = RunLogger(run_dir)

    print(f"\n{'='*60}")
    print(f"  Benefills Content Workflow V2")
    print(f"  {'[MOCK MODE]' if args.mock else ''}")
    print(f"  Output → {run_dir}")
    print(f"{'='*60}\n")

    try:
        # ── Step 1: Load Brand Context ──────────────────────────
        print("[1/6] Loading brand context...")
        brand_context = load_brand_context()
        run_log.log_step("load_brand_context", "success", {
            "brand": brand_context.get("brand_name")
        })
        logger.info("Brand context loaded.")

        # ── Step 2: Collect & Validate Inputs ───────────────────
        print("[2/6] Collecting inputs...")
        inputs = collect_inputs(args)
        run_log.log_step("collect_inputs", "success", {
            "links": len(inputs["links"]),
            "images": len(inputs["images"])
        })
        print(f"       Found {len(inputs['links'])} links, {len(inputs['images'])} images")

        all_analyses = []
        if inputs["topic"]:
            # ── Scratch Mode ────────────────────────────────────────
            print(f"[4/6] Generating concept for topic: '{inputs['topic']}'...")
            
            # Use 'analyze_inspo' analyzer for now, but we call generate_concept
            # Ideally we might want a separate factory for ideators, but reusing analyzer is fine
            analyzer = AnalyzerFactory.get_analyzer(
                provider=args.text_provider, mock=args.mock
            )
            
            concept = analyzer.generate_concept(inputs["topic"], brand_context)
            all_analyses.append(concept)
            print(f"       Concept generated for topic.")

        else:
            # ── Inspiration Mode ────────────────────────────────────
            # ── Step 3: Scrape / Load Inspiration ───────────────────
            print("[3/6] Fetching inspiration content...")
            scraper = ScraperFactory.get_scraper(mock=args.mock)
            scraped_dir = os.path.join(run_dir, "scraped")
            scraped_posts = []

            if inputs["links"] and not args.skip_scrape:
                scraped_posts.extend(scraper.scrape_posts(inputs["links"], scraped_dir))

            if inputs["images"]:
                scraped_posts.extend(scraper.load_local_images(inputs["images"], scraped_dir))

            if not scraped_posts:
                logger.error("No inspiration content could be loaded.")
                run_log.log_step("scrape", "failed", {"reason": "no content loaded"})
                run_log.save()
                sys.exit(1)

            run_log.log_step("scrape", "success", {
                "posts_scraped": len(scraped_posts)
            })
            print(f"       Loaded {len(scraped_posts)} inspiration posts")

            # ── Step 4: Analyze Inspiration ─────────────────────────
            print("[4/6] Analyzing inspiration content...")
            analyzer = AnalyzerFactory.get_analyzer(
                provider=args.text_provider, mock=args.mock
            )

            for i, post in enumerate(scraped_posts):
                print(f"       Analyzing post {i+1}/{len(scraped_posts)}...")
                analysis = analyzer.analyze(post.image_path, post.caption, brand_context)
                analysis["_source"] = post.to_dict()
                all_analyses.append(analysis)

        # Save combined analysis
        analysis_path = os.path.join(run_dir, "analysis.json")
        with open(analysis_path, 'w') as f:
            json.dump(all_analyses, f, indent=2)

        run_log.log_step("analyze", "success", {
            "analyses_count": len(all_analyses)
        })
        print(f"       Analysis saved to analysis.json")

        # ── Step 5: Generate Content Bundles ────────────────────
        print(f"[5/6] Generating {args.variants} post variants per inspiration...")
        caption_gen = CaptionGeneratorFactory.get_generator(
            provider=args.text_provider, mock=args.mock
        )
        image_gen = ImageGeneratorFactory.get_generator(
            provider=args.image_provider, mock=args.mock
        )
        reviewer = ReviewerFactory.get_reviewer(
            provider=args.text_provider, mock=args.mock
        )

        post_count = 0
        for a_idx, analysis in enumerate(all_analyses):
            # Generate captions
            captions = caption_gen.generate(analysis, brand_context, args.variants)

            for v_idx, variant in enumerate(captions):
                post_count += 1
                post_dir = os.path.join(run_dir, f"post_{post_count}")
                os.makedirs(post_dir, exist_ok=True)

                # Save caption
                caption_text = variant.get("caption", "")
                hashtags = variant.get("hashtags", "")
                full_caption = f"{caption_text}\n\n---\n{hashtags}" if hashtags else caption_text

                caption_path = os.path.join(post_dir, "caption.txt")
                with open(caption_path, 'w') as f:
                    f.write(full_caption)

                # Build image prompt from analysis
                image_prompt = build_image_prompt(analysis, brand_context)

                # Generate image (unless skipped)
                image_path = None
                if not args.skip_images:
                    image_path = os.path.join(post_dir, "image.png")
                    try:
                        image_gen.generate(image_prompt, image_path, style=args.style)
                    except Exception as e:
                        logger.error(f"Image generation failed for post {post_count}: {e}")
                        run_log.log_error(f"image_gen_post_{post_count}", str(e))
                        image_path = None

                # Review (unless skipped)
                review_data = {}
                if not args.skip_review:
                    try:
                        review_data = reviewer.review(
                            caption_text, image_prompt, analysis, brand_context
                        )
                    except Exception as e:
                        logger.error(f"Review failed for post {post_count}: {e}")
                        run_log.log_error(f"review_post_{post_count}", str(e))

                # Save metadata
                metadata = {
                    "post_number": post_count,
                    "variant": variant.get("variant", v_idx + 1),
                    "angle": variant.get("angle", "unknown"),
                    "style": args.style,
                    "image_provider": args.image_provider,
                    "text_provider": args.text_provider,
                    "image_prompt_used": image_prompt,
                    "image_generated": image_path is not None,
                    "review": review_data,
                    "inspiration_source": analysis.get("_source", {}).get("source_url", "unknown")
                }

                metadata_path = os.path.join(post_dir, "metadata.json")
                with open(metadata_path, 'w') as f:
                    json.dump(metadata, f, indent=2)

                # Print summary
                overall_score = review_data.get("overall_quality", {}).get("score", "N/A")
                print(f"       ✓ Post {post_count} ({variant.get('angle', '?')}) — Score: {overall_score}/10")

        run_log.log_step("generate", "success", {
            "posts_generated": post_count
        })

        # ── Step 6: Final Summary ───────────────────────────────
        print(f"\n[6/6] Pipeline complete!")
        run_log.log_step("complete", "success")
        log_path = run_log.save()

        print(f"\n{'='*60}")
        print(f"  ✅ DONE — {post_count} posts generated")
        print(f"  📁 Output: {run_dir}")
        print(f"  📋 Run log: {log_path}")
        print(f"{'='*60}\n")

        # Print generated captions for quick review
        print("── Quick Caption Preview ──\n")
        for i in range(1, post_count + 1):
            caption_file = os.path.join(run_dir, f"post_{i}", "caption.txt")
            if os.path.isfile(caption_file):
                with open(caption_file, 'r') as f:
                    content = f.read()
                # Show first 200 chars
                preview = content[:200] + "..." if len(content) > 200 else content
                print(f"Post {i}:")
                print(f"  {preview}\n")

    except KeyboardInterrupt:
        print("\n\n⚠️  Pipeline interrupted by user.")
        run_log.log_error("pipeline", "Interrupted by user")
        run_log.save()
        sys.exit(1)

    except Exception as e:
        logger.error(f"Pipeline failed: {str(e)}")
        run_log.log_error("pipeline", str(e))
        run_log.save()
        print(f"\n❌ ERROR: {str(e)}")
        print(f"   Check logs at: {run_dir}/run_log.json")
        sys.exit(1)


if __name__ == "__main__":
    main()
