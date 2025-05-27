
import os
import subprocess
import uuid

def download_video(url):
    """Download TikTok video and extract audio with UUID-based naming"""
    try:
        # Ensure tmp directory exists
        os.makedirs('/tmp', exist_ok=True)
        
        video_id = str(uuid.uuid4())
        video_path = f"/tmp/{video_id}.mp4"
        audio_path = f"/tmp/{video_id}.mp3"
        
        # Download video using yt-dlp
        download_cmd = [
            "yt-dlp", 
            "-f", "mp4",
            "-o", video_path,
            url
        ]
        subprocess.run(download_cmd, check=True)
        
        # Extract audio from video
        audio_cmd = [
            "ffmpeg", "-y", "-i", video_path, 
            "-q:a", "0", "-map", "a", 
            audio_path
        ]
        subprocess.run(audio_cmd, check=True)
        
        return video_path, audio_path
        
    except subprocess.CalledProcessError as e:
        raise Exception(f"Error downloading video: {e}")
    except Exception as e:
        raise Exception(f"Error in download process: {e}")
