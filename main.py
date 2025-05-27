
from flask import Flask, request, jsonify
import os
import uuid
import traceback
from download_video import download_video
from transcribe import transcribe_audio
from srt_to_ass import convert_srt_to_ass
from render_video import render_final_video
from send_telegram import send_to_telegram

app = Flask(__name__)

@app.route('/')
def home():
    return """
    <h1>🎵 TikTok Audio Caption Bot</h1>
    <p>Send a POST request to /process with JSON body:</p>
    <pre>{
  "url": "https://www.tiktok.com/@user/video/123456",
  "bot_token": "your_telegram_bot_token",
  "chat_id": "your_chat_id"
}</pre>
    <p>The bot will:</p>
    <ul>
        <li>✅ Download TikTok video</li>
        <li>✅ Extract audio</li> 
        <li>✅ Transcribe with Whisper.cpp</li>
        <li>✅ Create animated subtitles</li>
        <li>✅ Render final video</li>
        <li>✅ Send to Telegram</li>
    </ul>
    """

@app.route('/process', methods=['POST'])
def process_video():
    try:
        # Validate request
        data = request.get_json()
        if not data:
            return jsonify({'error': 'JSON data required'}), 400
        
        url = data.get('url')
        bot_token = data.get('bot_token')
        chat_id = data.get('chat_id')
        
        if not url:
            return jsonify({'error': 'TikTok URL is required'}), 400
        if not bot_token:
            return jsonify({'error': 'Telegram bot token is required'}), 400
        if not chat_id:
            return jsonify({'error': 'Telegram chat ID is required'}), 400

        # Process video
        print(f"🎬 Processing TikTok video: {url}")
        
        # Step 1: Download video and extract audio
        print("📥 Downloading video and extracting audio...")
        video_path, audio_path = download_video(url)
        
        # Step 2: Transcribe audio using whisper.cpp
        print("🎙️ Transcribing audio...")
        srt_path = transcribe_audio(audio_path)
        
        # Step 3: Convert SRT to ASS with animations
        print("✨ Creating animated subtitles...")
        ass_path = convert_srt_to_ass(srt_path)
        
        # Step 4: Render final video
        print("🎥 Rendering final video...")
        final_video_path = render_final_video(audio_path, ass_path)
        
        # Step 5: Send to Telegram
        print("📤 Sending to Telegram...")
        send_to_telegram(bot_token, chat_id, final_video_path)
        
        # Cleanup temporary files
        cleanup_files([video_path, audio_path, srt_path, ass_path, final_video_path])
        
        return jsonify({
            'status': 'success',
            'message': '✅ Video processed and sent to Telegram!'
        })
        
    except Exception as e:
        error_msg = f"❌ Error: {str(e)}"
        print(error_msg)
        print(traceback.format_exc())
        return jsonify({'error': error_msg}), 500

def cleanup_files(file_paths):
    """Clean up temporary files"""
    for file_path in file_paths:
        try:
            if file_path and os.path.exists(file_path):
                os.remove(file_path)
                print(f"🗑️ Cleaned up: {file_path}")
        except Exception as e:
            print(f"⚠️ Failed to cleanup {file_path}: {e}")

if __name__ == '__main__':
    # Ensure tmp directory exists
    os.makedirs('/tmp', exist_ok=True)
    print("🚀 Starting TikTok Audio Caption Bot...")
    app.run(host='0.0.0.0', port=5000, debug=True)
