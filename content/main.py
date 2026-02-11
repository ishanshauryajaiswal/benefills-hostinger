import argparse
import os
import sys
from modules.detective import Detective
from modules.scripting import ScriptingFactory
from modules.audio import AudioFactory
from modules.video import VideoFactory
from modules.assembly import VideoEditor
from modules.designer import ImageFactory
from modules.image_prompts import ImagePrompts

from modules.logger import setup_logger

logger = setup_logger('engine', 'content/logs/engine.log')

def main():
    parser = argparse.ArgumentParser(description="Benefills Brand Presence Engine")
    parser.add_argument("--topic", type=str, required=True, help="Topic for the Instagram Content")
    parser.add_argument("--format", type=str, choices=["reel", "carousel"], default="carousel", help="Format of content")
    parser.add_argument("--style", type=str, choices=["poster", "flatlay", "cookbook", "grid", "editorial", "amazon", "lifestyle"], default="poster", help="Style of image generation")
    parser.add_argument("--image-provider", type=str, choices=["dalle", "google"], default="google", help="Provider for image generation")
    parser.add_argument("--mock", action="store_true", help="Run in mock mode without API calls")
    args = parser.parse_args()

    logger.info(f"Starting {args.format} generation for topic: {args.topic} (Mock: {args.mock})")

    try:
        # 1. Intake Context
        print(f"[1/5] Analyzing brand context for {args.format}...")
        root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        detective = Detective(root_dir)
        brand_context = detective.analyze()
        logger.info("Context intake complete.")

        # 2. Generate Content Script/Plan
        print(f"[2/5] Generating {args.format} plan for topic: {args.topic}...")
        provider_type = "mock" if args.mock else "claude"
        scripting = ScriptingFactory.get_provider(provider_type)
        content_plan = scripting.generate_script(args.topic, brand_context, args.format)
        
        if args.format == "carousel":
            # Save the carousel plan to the outputs folder
            topic_slug = args.topic.lower().replace(" ", "_")
            filename = topic_slug + ".md"
            carousel_dir = os.path.join(root_dir, "content/outputs/carousels", topic_slug)
            os.makedirs(carousel_dir, exist_ok=True)
            output_file = os.path.join(carousel_dir, filename)
            
            with open(output_file, 'w') as f:
                f.write(content_plan)
                
            print(f"\n--- CAROUSEL PLAN SAVED ---\nLocation: {output_file}\n")
            logger.info(f"Carousel plan saved to {output_file}")

            # Step 2b: Generate Images for Slides
            print(f"[2b/5] Extracting visual prompts and generating images...")
            image_provider = "mock" if args.mock else args.image_provider
            designer = ImageFactory.get_provider(image_provider)
            
            # More robust parsing for Slide visuals
            slides = content_plan.split("## SLIDE")
            for i, slide in enumerate(slides[1:], 1):
                prompt_block = None
                # Check for various common formatting patterns (case-insensitive)
                slide_lower = slide.lower()
                for marker in ["visual prompt:", "**visual prompt:**", "### visual prompt:"]:
                    if marker in slide_lower:
                        parts = slide_lower.split(marker)
                        if len(parts) > 1:
                            # Extract matching case from original slide
                            start_idx = slide_lower.find(marker) + len(marker)
                            content_after = slide[start_idx:].strip().split("\n\n")[0].split("###")[0].strip()
                            # Clean up leading bullet points or markers
                            lines = content_after.split('\n')
                            cleaned_lines = [l.strip().lstrip('-').lstrip('*').strip() for l in lines]
                            prompt_block = " ".join(cleaned_lines)
                            if prompt_block:
                                break
                
                if prompt_block:
                    # Refine prompt using the selected style strategy
                    refined_prompt = ImagePrompts.get_prompt(args.style, f"'Benefills' brand: {prompt_block}")
                    img_filename = f"slide_{i}.png"
                    img_path = os.path.join(carousel_dir, img_filename)
                    
                    print(f"Generating image for Slide {i}...")
                    designer.generate_image(refined_prompt, img_path)
                    logger.info(f"Generated image for Slide {i}: {img_path}")
                else:
                    logger.warning(f"No visual prompt found for Slide {i}")

            print(f"\nSUCCESS! Carousel folder ready at: {carousel_dir}")
            sys.exit(0)

        # 3. Synthesize Audio (Reels Only)
        print("[3/5] Synthesizing audio...")
        audio_provider = "mock" if args.mock else "elevenlabs"
        audio_engine = AudioFactory.get_provider(audio_provider)
        audio_path = os.path.join(root_dir, "content/temp/voiceover.mp3")
        audio_engine.synthesize(content_plan, audio_path)
        logger.info("Audio synthesis complete.")

        # 4. Generate Video (Reels Only)
        print("[4/5] Generating digital twin video...")
        video_provider = "mock" if args.mock else "heygen"
        video_engine = VideoFactory.get_provider(video_provider)
        video_path = os.path.join(root_dir, "content/temp/avatar.mp4")
        video_engine.generate_video(content_plan, audio_path, video_path)
        logger.info("Video generation complete.")

        # 5. Assemble Final Reel (Reels Only)
        print("[5/5] Assembling final reel...")
        editor = VideoEditor(os.path.join(root_dir, "content/assets"))
        output_path = editor.assemble(video_path, audio_path, args.topic.replace(" ", "_"))
        logger.info(f"Assembly complete. Output: {output_path}")

        print(f"\nSUCCESS! Reel generated at: {output_path}")

    except Exception as e:
        logger.error(f"Pipeline failed: {str(e)}")
        print(f"\nERROR: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
