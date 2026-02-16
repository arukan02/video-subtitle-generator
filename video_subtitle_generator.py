"""
VIDEO SUBTITLE GENERATOR - Learning Edition
============================================
This tool takes raw video footage and:
1. Transcribes the audio using Whisper
2. Translates to Japanese/Korean
3. Adds bilingual subtitles to the video

LEARNING PATH:
- Start with Part 1 (Setup)
- Move to Part 2 (Audio extraction)
- Then Part 3 (Transcription)
- Part 4 (Translation)
- Finally Part 5 (Adding subtitles)

Each section has TODO comments to guide you!
"""

# ============================================================================
# PART 1: IMPORTS AND SETUP
# ============================================================================
# TODO: Install these libraries first:
# pip install moviepy
# pip install openai-whisper
# pip install deep-translator
# pip install pillow

# TODO: Import the necessary libraries here
from moviepy import VideoFileClip, TextClip, CompositeVideoClip
import whisper
from deep_translator import GoogleTranslator
import os


# ============================================================================
# PART 2: EXTRACT AUDIO FROM VIDEO
# ============================================================================

def extract_audio(video_path, audio_output_path="temp_audio.wav"):
    """
    Extract audio from video file for transcription.
    
    Args:
        video_path: Path to your raw video file
        audio_output_path: Where to save the extracted audio
        
    Returns:
        Path to the extracted audio file
        
    LEARNING NOTES:
    - MoviePy can load video files with VideoFileClip()
    - The .audio attribute gives you the audio track
    - .write_audiofile() saves it to disk
    """
    
    # TODO: Load the video file using VideoFileClip
    video = VideoFileClip(video_path)
    
    # TODO: Extract the audio track
    audio = video.audio
    
    # TODO: Write the audio to a file
    audio.write_audiofile(audio_output_path)
    
    # TODO: Close the video file to free memory
    video.close()
    
    # TODO: Return the path to the audio file
    return audio_output_path
    
    #pass  # Remove this when you add your code


# ============================================================================
# PART 3: TRANSCRIBE AUDIO USING WHISPER
# ============================================================================

def transcribe_audio(audio_path, language="en"):
    """
    Use OpenAI's Whisper to transcribe audio to text.
    
    Args:
        audio_path: Path to the audio file
        language: Language code (en, ja, ko, etc.)
        
    Returns:
        Dictionary with transcription results including:
        - text: Full transcription
        - segments: List of timed segments (for precise subtitle timing)
        
    LEARNING NOTES:
    - Whisper models: tiny, base, small, medium, large
    - Smaller models are faster but less accurate
    - Start with "base" model for learning
    - segments contain start/end times for each phrase
    """
    
    # TODO: Load the Whisper model
    # model = whisper.load_model("base")  # Try "base" first, then upgrade to "small" or "medium"
    model = whisper.load_model('base')
    
    # TODO: Transcribe the audio
    # result = model.transcribe(audio_path, language=language)
    result = model.transcribe(audio_path, language=language)

    # TODO: Print the transcription to see what you got
    # print("Transcription:", result["text"])
    print("Transcription:", result["text"])
    
    # TODO: Return the result dictionary
    # return result
    return result
    
    #pass  # Remove this when you add your code


# ============================================================================
# PART 4: TRANSLATE TEXT
# ============================================================================

def translate_segments(segments, target_language="ja"):
    """
    Translate each transcription segment to target language.
    
    Args:
        segments: List of segments from Whisper transcription
        target_language: Target language code (ja=Japanese, ko=Korean)
        
    Returns:
        List of segments with added 'translation' field
        
    LEARNING NOTES:
    - GoogleTranslator is free and good for learning
    - Each segment has: start, end, text
    - We'll add a 'translation' field to each segment
    """
    
    # TODO: Create a translator object
    translator = GoogleTranslator(source='auto', target=target_language)
    
    # TODO: Loop through each segment
            # TODO: Get the text from the segment
    for segment in segments:
        original_text = segment['text']
        
        # TODO: Translate the text
        translated_text = translator.translate(original_text)
        
        # TODO: Add translation to the segment
        segment['translation'] = translated_text
        
        # TODO: Print to see progress (optional)
        print(f"Original: {original_text}")
        print(f"Translation: {translated_text}\n")
    
    # TODO: Return the segments with translations
    return segments
    
    #pass  # Remove this when you add your code


# ============================================================================
# PART 5: CREATE SUBTITLE CLIPS
# ============================================================================

def create_subtitle_clips(segments, video_width, video_height):
    """
    Create TextClip objects for each subtitle segment.
    
    Args:
        segments: List of segments with text and translations
        video_width: Width of the video (for positioning)
        video_height: Height of the video (for positioning)
        
    Returns:
        List of TextClip objects with proper timing
        
    LEARNING NOTES:
    - TextClip creates text overlays
    - with_position() controls where text appears
    - with_start() and with_end() control when text appears
    - We'll put original text at bottom, translation above it
    """
    
    subtitle_clips = []
    
    # TODO: Loop through each segment
    for segment in segments:
        start_time = segment['start']
        end_time = segment['end']
        original_text = segment['text']
        translated_text = segment.get('translation', '')
    # for segment in segments:
        # Get timing information
        # start_time = segment['start']
        # end_time = segment['end']
        # original_text = segment['text']
        # translated_text = segment.get('translation', '')
        
        # TODO: Create TextClip for original text (bottom)
        txt_clip_original = TextClip(
            text=original_text,
            font_size=32,
            color='white',
            bg_color='black',
            font='C:/Windows/Fonts/arial.ttf',
            method='label',
            size=(video_width - 40, None)
        )
        
        # TODO: Position at bottom of video
        txt_clip_original = txt_clip_original.with_position(('center', video_height - 100))
        txt_clip_original = txt_clip_original.with_start(start_time).with_end(end_time)
        
        # TODO: Create TextClip for translation (above original)
        txt_clip_translation = TextClip(
            text=translated_text,
            font_size=28,
            color='yellow',
            bg_color='black',
            font='C:/Windows/Fonts/NotoSansJP-VF.ttf',  # IMPORTANT: Use a font that supports your target language!
            method='caption',
            size=(video_width - 40, None)
        )
        
        # TODO: Position above the original text
        txt_clip_translation = txt_clip_translation.with_position(('center', video_height - 150))
        txt_clip_translation = txt_clip_translation.with_start(start_time).with_end(end_time)
        
        # TODO: Add both clips to the list
        subtitle_clips.append(txt_clip_original)
        subtitle_clips.append(txt_clip_translation)
    
    # TODO: Return the list of subtitle clips
    return subtitle_clips
    
    #pass  # Remove this when you add your code


# ============================================================================
# PART 6: COMBINE EVERYTHING
# ============================================================================

def add_subtitles_to_video(video_path, subtitle_clips, output_path="output_video.mp4"):
    """
    Combine the original video with subtitle clips.
    
    Args:
        video_path: Path to original video
        subtitle_clips: List of TextClip objects
        output_path: Where to save the final video
        
    LEARNING NOTES:
    - CompositeVideoClip layers multiple clips together
    - The original video is the base layer
    - Subtitles are overlaid on top
    """
    
    # TODO: Load the original video
    video = VideoFileClip(video_path)
    
    # TODO: Composite the video with all subtitle clips
    final_video = CompositeVideoClip([video] + subtitle_clips)
    
    # TODO: Write the final video to file
    final_video.write_videofile(
        output_path,
        codec='libx264',
        audio_codec='aac',
        fps=video.fps
    )
    
    # TODO: Close video files to free memory
    video.close()
    final_video.close()
    
    #pass  # Remove this when you add your code


# ============================================================================
# PART 7: MAIN FUNCTION - PUTTING IT ALL TOGETHER
# ============================================================================

def main(video_path, target_language="ja", output_path="final_video.mp4"):
    """
    Main function that orchestrates the entire process.
    
    This is where you'll call all the functions in order!
    """
    
    print("Starting video subtitle generation...")
    
    # TODO: Step 1 - Extract audio
    print("\n[1/5] Extracting audio...")
    audio_path = extract_audio(video_path)
    
    # TODO: Step 2 - Transcribe audio
    print("\n[2/5] Transcribing audio...")
    transcription = transcribe_audio(audio_path)
    
    # TODO: Step 3 - Translate segments
    print("\n[3/5] Translating to target language...")
    segments_with_translation = translate_segments(
        transcription['segments'],
        target_language=target_language
    )
    
    # TODO: Step 4 - Load video to get dimensions
    print("\n[4/5] Creating subtitle clips...")
    video = VideoFileClip(video_path)
    video_width, video_height = video.size
    video.close()
    
    # TODO: Create subtitle clips
    subtitle_clips = create_subtitle_clips(
        segments_with_translation,
        video_width,
        video_height
    )
    
    # TODO: Step 5 - Combine everything
    print("\n[5/5] Adding subtitles to video...")
    add_subtitles_to_video(video_path, subtitle_clips, output_path)
    
    # TODO: Clean up temporary audio file
    if os.path.exists("temp_audio.wav"):
        os.remove("temp_audio.wav")
    
    print(f"\n✅ Done! Video saved to: {output_path}")


# ============================================================================
# RUN THE PROGRAM
# ============================================================================

if __name__ == "__main__":
    # TODO: Replace with your actual video file path
    input_video = "test.MOV"
    
    # TODO: Choose target language: "ja" for Japanese, "ko" for Korean
    target_lang = "ja"
    
    # TODO: Choose output filename
    output_video = "test_with_subtitles.mp4"
    
    # TODO: Uncomment this line when ready to run
    main(input_video, target_lang, output_video)
    
    print("Remove the TODOs and uncomment the code to run!")


# ============================================================================
# NEXT STEPS FOR LEARNING
# ============================================================================
"""
BEGINNER PATH:
1. Start by uncommenting Part 2 (extract_audio) and test it
2. Then uncomment Part 3 (transcribe_audio) and see the transcription
3. Continue one part at a time
4. Test each function individually before moving to the next

CHALLENGES TO TRY AFTER BASIC VERSION WORKS:
- Add error handling (what if video file doesn't exist?)
- Support different font files for Japanese/Korean
- Add styling options (font color, size, position)
- Save transcription/translation to a file (JSON or SRT format)
- Add a progress bar using tqdm library
- Handle long videos by chunking audio
- Add a config file for settings instead of hardcoding

IMPORTANT FONT NOTE:
For Japanese/Korean text to display correctly, you need fonts that support
those characters. Common fonts:
- Japanese: "MS Gothic", "Yu Gothic", "Noto Sans JP"
- Korean: "Malgun Gothic", "Noto Sans KR"

Download these fonts and specify the full path in TextClip's font parameter.
"""
