import subprocess
import os

class VideoEditor:
    """
    Handles FFmpeg operations for assembly, captions, and B-roll overlays.
    """
    def __init__(self, assets_dir):
        self.assets_dir = assets_dir
        self.logo_path = os.path.join(assets_dir, "logos/watermark.png")

    def assemble(self, avatar_video: str, audio_file: str, output_name: str):
        output_path = os.path.normpath(os.path.join(os.path.dirname(__file__), f"../outputs/{output_name}.mp4"))
        
        # Check if logo exists for watermark
        logo_filter = ""
        input_args = ["-i", avatar_video, "-i", audio_file]
        
        if os.path.exists(self.logo_path):
            input_args += ["-i", self.logo_path]
            # Overlay logo in top right
            logo_filter = "[0:v][2:v]overlay=W-w-10:10"
        else:
            logo_filter = "[0:v]null"

        # Base command for 9:16 aspect ratio
        cmd = [
            "ffmpeg", "-y"
        ] + input_args + [
            "-filter_complex", f"{logo_filter},scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920",
            "-c:v", "libx264", "-pix_fmt", "yuv420p",
            "-c:a", "aac", "-strict", "experimental",
            output_path
        ]
        
        print(f"Executing FFmpeg: {' '.join(cmd)}")
        try:
            subprocess.run(cmd, check=True, capture_output=True)
            logger.info("FFmpeg assembly successful.")
        except subprocess.CalledProcessError as e:
            logger.error(f"FFmpeg failed: {e.stderr.decode()}")
            print(f"FFmpeg error: See logs for details.")
        return output_path

    def add_captions(self, video_path: str, transcript: str):
        # Implementation for generating .srt and burning it into the video
        pass

    def add_broll(self, video_path: str, broll_mapping: list):
        # Implementation for overlaying B-roll based on timestamps/visual cues
        pass
