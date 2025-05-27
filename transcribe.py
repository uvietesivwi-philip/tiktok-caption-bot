
import subprocess
import os
import uuid

def transcribe_audio(audio_path):
    """Transcribe audio using Whisper.cpp (local, unlimited, free)"""
    try:
        # Generate unique SRT filename
        srt_path = f"/tmp/{uuid.uuid4()}.srt"
        
        # Check if whisper.cpp executable exists
        whisper_executable = "./whisper.cpp/build/bin/whisper-cli"
        if not os.path.exists(whisper_executable):
            # Try alternative path
            whisper_executable = "./whisper.cpp/main"
            if not os.path.exists(whisper_executable):
                raise Exception("Whisper.cpp executable not found. Run: cd whisper.cpp && make")
        
        # Check if model exists
        model_path = "./whisper.cpp/models/ggml-base.en.bin"
        if not os.path.exists(model_path):
            raise Exception("Whisper model not found. Run: cd whisper.cpp && ./models/download-ggml-model.sh base.en")
        
        print(f"🎙️ Transcribing with whisper.cpp: {audio_path}")
        
        # Run whisper.cpp transcription
        command = [
            whisper_executable,
            "-m", model_path,
            "-f", audio_path,
            "-osrt"
        ]
        
        print(f"Running command: {' '.join(command)}")
        result = subprocess.run(command, capture_output=True, text=True)
        
        print(f"Whisper.cpp stdout: {result.stdout}")
        print(f"Whisper.cpp stderr: {result.stderr}")
        print(f"Whisper.cpp return code: {result.returncode}")
        
        # whisper.cpp creates the SRT file by adding .srt to the full audio filename
        generated_srt = f"{audio_path}.srt"
        
        print(f"Looking for SRT file at: {generated_srt}")
        print(f"SRT file exists: {os.path.exists(generated_srt)}")
        
        # List files in the same directory to see what was created
        audio_dir = os.path.dirname(audio_path)
        print(f"Files in {audio_dir}: {os.listdir(audio_dir)}")
        
        # Check if SRT file was created
        if os.path.exists(generated_srt):
            # Move to our expected location
            os.rename(generated_srt, srt_path)
        else:
            # If whisper.cpp failed, raise with detailed error
            if result.returncode != 0:
                raise Exception(f"Whisper.cpp failed with return code {result.returncode}: {result.stderr}")
            else:
                raise Exception("SRT file was not created by whisper.cpp")
        
        print(f"✅ Transcription complete: {srt_path}")
        return srt_path
        
    except subprocess.CalledProcessError as e:
        raise Exception(f"Whisper.cpp transcription failed: {e.stderr}")
    except Exception as e:
        raise Exception(f"Transcription error: {e}")
