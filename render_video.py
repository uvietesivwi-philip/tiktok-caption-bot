
import subprocess
import os
import uuid

def render_final_video(audio_path, ass_path):
    """Render final video with animated subtitles overlaid on audio waveform"""
    try:
        # Generate unique output filename
        output_path = f"/tmp/{uuid.uuid4()}.mp4"
        
        print(f"🎥 Rendering final video with subtitles...")
        
        # Create a video from audio with waveform visualization and subtitles
        # Using FFmpeg to create waveform video with ASS subtitles
        ffmpeg_cmd = [
            "ffmpeg", "-y",
            "-i", audio_path,
            "-filter_complex", 
            f"[0:a]showwaves=s=1080x1920:mode=cline:colors=#0080FF:scale=lin,format=yuv420p[v];[v]subtitles={ass_path}:force_style='Fontsize=72,PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,Outline=3,Shadow=2,Alignment=2,MarginV=100'[out]",
            "-map", "[out]",
            "-map", "0:a",
            "-c:v", "libx264",
            "-c:a", "aac",
            "-preset", "fast",
            "-crf", "23",
            "-r", "30",
            "-t", "60",  # Limit to 60 seconds to avoid huge files
            output_path
        ]
        
        print(f"🔄 Running FFmpeg command...")
        result = subprocess.run(ffmpeg_cmd, capture_output=True, text=True, check=True)
        
        if not os.path.exists(output_path):
            raise Exception("Output video file was not created")
        
        file_size = os.path.getsize(output_path) / (1024 * 1024)  # Size in MB
        print(f"✅ Video rendered successfully: {output_path} ({file_size:.1f}MB)")
        
        return output_path
        
    except subprocess.CalledProcessError as e:
        raise Exception(f"FFmpeg rendering failed: {e.stderr}")
    except Exception as e:
        raise Exception(f"Video rendering error: {e}")
