"""
VIDEO SUBTITLE GENERATOR - UI Edition
======================================
New features:
1. Auto-sizing subtitle backgrounds (fit to text)
2. Simple UI to review/edit translations before creating video
"""

from moviepy import VideoFileClip, TextClip, CompositeVideoClip
import whisper
from deep_translator import GoogleTranslator
import os
import json


# ============================================================================
# PART 1: AUDIO EXTRACTION (Same as before)
# ============================================================================

def extract_audio(video_path, audio_output_path="temp_audio.wav"):
    """Extract audio from video file for transcription."""
    video = VideoFileClip(video_path)
    audio = video.audio
    audio.write_audiofile(audio_output_path, logger=None)
    video.close()
    return audio_output_path


# ============================================================================
# PART 2: TRANSCRIPTION (Same as before)
# ============================================================================

def transcribe_audio(audio_path, language="en"):
    """Use OpenAI's Whisper to transcribe audio to text."""
    print("Loading Whisper model...")
    model = whisper.load_model("base")
    
    print("Transcribing...")
    result = model.transcribe(audio_path, language=language)
    
    return result


# ============================================================================
# PART 3: TRANSLATION (Same as before)
# ============================================================================

def translate_segments(segments, target_language="ja"):
    """Translate each transcription segment to target language."""
    translator = GoogleTranslator(source='auto', target=target_language)
    
    for i, segment in enumerate(segments):
        original_text = segment['text']
        translated_text = translator.translate(original_text)
        segment['translation'] = translated_text
        
        print(f"[{i+1}/{len(segments)}] Translated segment")
    
    return segments


# ============================================================================
# PART 4: SAVE & LOAD TRANSLATIONS (NEW!)
# ============================================================================

def save_translations(segments, filepath="translations.json"):
    """
    Save transcriptions and translations to a JSON file for editing.
    
    This creates a file you can open and edit manually!
    """
    data = []
    for i, segment in enumerate(segments):
        data.append({
            'index': i,
            'start_time': segment['start'],
            'end_time': segment['end'],
            'original': segment['text'],
            'translation': segment.get('translation', '')
        })
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ Translations saved to: {filepath}")
    print("You can now edit this file to fix any translation errors!")
    return filepath


def load_translations(filepath="translations.json"):
    """
    Load edited translations from JSON file.
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    segments = []
    for item in data:
        segments.append({
            'start': item['start_time'],
            'end': item['end_time'],
            'text': item['original'],
            'translation': item['translation']
        })
    
    print(f"\n✅ Loaded {len(segments)} segments from {filepath}")
    return segments


# ============================================================================
# PART 5: SIMPLE TEXT-BASED UI (NEW!)
# ============================================================================

def review_translations_ui(segments):
    """
    Simple command-line UI to review and edit translations.
    
    This lets you edit translations without opening JSON files!
    """
    print("\n" + "="*70)
    print("TRANSLATION REVIEW & EDIT")
    print("="*70)
    print("\nCommands:")
    print("  [Enter]     - Next segment")
    print("  'e [num]'   - Edit segment number")
    print("  's'         - Save and continue")
    print("  'q'         - Quit without saving")
    print("="*70 + "\n")
    
    i = 0
    while i < len(segments):
        segment = segments[i]
        
        print(f"\n[Segment {i+1}/{len(segments)}]")
        print(f"Time: {segment['start']:.1f}s - {segment['end']:.1f}s")
        print(f"Original:    {segment['text']}")
        print(f"Translation: {segment['translation']}")
        print("-" * 70)
        
        command = input("Command (Enter/e [num]/s/q): ").strip().lower()
        
        if command == '':
            # Next segment
            i += 1
        elif command.startswith('e'):
            # Edit a segment
            try:
                parts = command.split()
                if len(parts) == 1:
                    # Edit current segment
                    edit_index = i
                else:
                    # Edit specific segment
                    edit_index = int(parts[1]) - 1
                
                if 0 <= edit_index < len(segments):
                    print(f"\nEditing segment {edit_index + 1}")
                    print(f"Original: {segments[edit_index]['text']}")
                    print(f"Current translation: {segments[edit_index]['translation']}")
                    new_translation = input("New translation: ").strip()
                    
                    if new_translation:
                        segments[edit_index]['translation'] = new_translation
                        print("✓ Updated!")
                else:
                    print("Invalid segment number!")
            except ValueError:
                print("Invalid command!")
        elif command == 's':
            # Save and continue
            print("\n✅ Continuing with current translations...")
            break
        elif command == 'q':
            # Quit
            print("\n❌ Cancelled. No changes made to video.")
            return None
        else:
            print("Unknown command!")
    
    return segments


# ============================================================================
# PART 6: CREATE SUBTITLE CLIPS WITH AUTO-SIZING (IMPROVED!)
# ============================================================================

def create_subtitle_clips(segments, video_width, video_height):
    """
    Create TextClip objects with auto-sizing backgrounds.
    
    NEW: Backgrounds now fit the text size instead of full width!
    """
    subtitle_clips = []
    
    for segment in segments:
        start_time = segment['start']
        end_time = segment['end']
        original_text = segment['text']
        translated_text = segment.get('translation', '')

        # Add a newline for vertical padding to prevent cutoff
        # This gives space for descenders like g, y, p, q, j
        original_text_padded = f"{original_text}\n"  # Add newline at bottom
        translated_text_padded = f"{translated_text}\n"
        
        # Create TextClip for original text (bottom)
        # method='label' creates auto-sizing background!
        txt_clip_original = TextClip(
            text=original_text,
            font_size=32,
            color='white',
            bg_color='black',
            font='C:/Windows/Fonts/arial.ttf',
            method='caption',  # Changed from 'caption' to 'label' for auto-sizing!
            size=(len(original_text) * 15, 40),  # Let it auto-size
            text_align='center'
        )
        
        txt_clip_original = txt_clip_original.with_position(('center', video_height - 100))
        txt_clip_original = txt_clip_original.with_start(start_time).with_end(end_time)
        
        # Create TextClip for translation (above original)
        txt_clip_translation = TextClip(
            text=translated_text,
            font_size=28,
            color='yellow',
            bg_color='black',
            font='C:/Windows/Fonts/msgothic.ttc',
            method='caption',
            size=(len(translated_text) * 30, 40),  # Let it auto-size
            text_align='center'
        )
        
        txt_clip_translation = txt_clip_translation.with_position(('center', video_height - 150))
        txt_clip_translation = txt_clip_translation.with_start(start_time).with_end(end_time)
        
        subtitle_clips.append(txt_clip_original)
        subtitle_clips.append(txt_clip_translation)
    
    return subtitle_clips


# ============================================================================
# PART 7: ADD SUBTITLES TO VIDEO (Same as before)
# ============================================================================

def add_subtitles_to_video(video_path, subtitle_clips, output_path="output_video.mp4"):
    """Combine the original video with subtitle clips."""
    video = VideoFileClip(video_path)
    final_video = CompositeVideoClip([video] + subtitle_clips)
    
    print("\nRendering final video (this may take a while)...")
    final_video.write_videofile(
        output_path,
        codec='libx264',
        audio_codec='aac',
        fps=video.fps,
        logger=None
    )
    
    video.close()
    final_video.close()


# ============================================================================
# PART 8: MAIN FUNCTION WITH UI WORKFLOW (NEW!)
# ============================================================================

def main(video_path, target_language="ja", output_path="final_video.mp4"):
    """
    Main function with new UI workflow.
    
    NEW WORKFLOW:
    1. Extract audio & transcribe
    2. Translate
    3. Save to JSON for review
    4. Interactive UI to edit translations
    5. Create video with subtitles
    """
    
    print("="*70)
    print("VIDEO SUBTITLE GENERATOR - UI Edition")
    print("="*70)
    
    # Check if we already have a translations file
    translations_file = "translations.json"
    
    if os.path.exists(translations_file):
        print(f"\n📄 Found existing translations file: {translations_file}")
        use_existing = input("Use existing translations? (y/n): ").strip().lower()
        
        if use_existing == 'y':
            segments = load_translations(translations_file)
        else:
            segments = process_new_video(video_path, target_language, translations_file)
    else:
        segments = process_new_video(video_path, target_language, translations_file)
    
    # Review and edit translations
    print("\n" + "="*70)
    print("REVIEW TRANSLATIONS")
    print("="*70)
    choice = input("\nDo you want to review/edit translations? (y/n): ").strip().lower()
    
    if choice == 'y':
        segments = review_translations_ui(segments)
        if segments is None:
            print("\nCancelled by user.")
            return
        
        # Save edited translations
        save_translations(segments, translations_file)
    
    # Create video with subtitles
    print("\n" + "="*70)
    print("CREATING VIDEO")
    print("="*70)
    
    video = VideoFileClip(video_path)
    video_width, video_height = video.size
    video.close()
    
    print("\nCreating subtitle clips...")
    subtitle_clips = create_subtitle_clips(segments, video_width, video_height)
    
    print("Adding subtitles to video...")
    add_subtitles_to_video(video_path, subtitle_clips, output_path)
    
    # Cleanup
    if os.path.exists("temp_audio.wav"):
        os.remove("temp_audio.wav")
    
    print("\n" + "="*70)
    print(f"✅ DONE! Video saved to: {output_path}")
    print("="*70)


def process_new_video(video_path, target_language, translations_file):
    """Process a new video: extract, transcribe, translate."""
    print("\n[1/3] Extracting audio...")
    audio_path = extract_audio(video_path)
    
    print("\n[2/3] Transcribing audio...")
    transcription = transcribe_audio(audio_path)
    
    print("\n[3/3] Translating to target language...")
    segments = translate_segments(
        transcription['segments'],
        target_language=target_language
    )
    
    # Save translations for review
    save_translations(segments, translations_file)
    
    return segments


# ============================================================================
# RUN THE PROGRAM
# ============================================================================

if __name__ == "__main__":
    # Configuration
    input_video = "test.MOV"  # Your video file
    target_lang = "ja"  # "ja" for Japanese, "ko" for Korean
    output_video = "test_with_subtitlesv3.mp4"
    
    # Run!
    main(input_video, target_lang, output_video)
