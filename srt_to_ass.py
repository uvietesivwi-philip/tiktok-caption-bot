
import pysrt
import re
import os
import uuid

def convert_srt_to_ass(srt_path):
    """Convert SRT to ASS with animations and styling"""
    try:
        ass_path = f"/tmp/{uuid.uuid4()}.ass"
        
        print(f"✨ Converting SRT to ASS: {srt_path}")
        
        # Read SRT file
        subs = pysrt.open(srt_path, encoding='utf-8')
        
        # Create ASS file with styling
        with open(ass_path, 'w', encoding='utf-8') as f:
            # ASS header with styling
            f.write("""[Script Info]
Title: TikTok Captions
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Arial Black,72,&H00FFFFFF,&H000080FF,&H00000000,&H80000000,-1,0,0,0,100,100,0,0,1,3,2,2,30,30,100,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
""")
            
            def format_ass_time(pysrt_time):
                """Convert pysrt time to ASS format"""
                return f"{pysrt_time.hours:01d}:{pysrt_time.minutes:02d}:{pysrt_time.seconds:02d}.{int(pysrt_time.milliseconds/10):02d}"
            
            for sub in subs:
                # Clean the subtitle text
                text = sub.text.replace('\n', ' ').strip()
                
                # Split into words for karaoke effect
                words = re.findall(r'\S+', text)
                
                if not words:
                    continue
                
                # Calculate timing for karaoke effect
                subtitle_duration = sub.end.ordinal - sub.start.ordinal  # in milliseconds
                words_count = len(words)
                
                if words_count > 0:
                    time_per_word = max(subtitle_duration // words_count, 200)  # minimum 200ms per word
                    k_units = max(time_per_word // 10, 20)  # ASS karaoke units (centiseconds)
                    
                    # Create karaoke text with blue highlighting effect
                    karaoke_text = ""
                    for word in words:
                        karaoke_text += f"{{\\k{k_units}\\c&H0080FF&}}{word} "
                    
                    # Add the dialogue line with center alignment
                    dialogue_line = f"Dialogue: 0,{format_ass_time(sub.start)},{format_ass_time(sub.end)},Default,,0,0,0,,{karaoke_text.strip()}"
                    f.write(dialogue_line + "\n")
        
        print(f"✅ ASS file created: {ass_path}")
        return ass_path
        
    except Exception as e:
        raise Exception(f"Error converting SRT to ASS: {e}")
