# Video Subtitle Generator

An AI-powered tool that automatically generates bilingual subtitles for videos using OpenAI's Whisper and Google Translate.

## Features

- Automatic speech-to-text transcription using Whisper
- Translation to Japanese/Korean
- Interactive UI to review and edit translations
- Auto-sizing subtitle backgrounds
- Bold, readable subtitles

## Requirements

- Python 3.8+
- FFmpeg

## Installation
```bash
pip install moviepy
pip install openai-whisper
pip install deep-translator
```

## Usage
```bash
python video_subtitle_generator_ui.py
```

Edit the configuration in the script:
- `input_video`: Path to your video file
- `target_lang`: "ja" for Japanese, "ko" for Korean
- `output_video`: Output filename

## How It Works

1. Extracts audio from video
2. Transcribes using Whisper AI
3. Translates to target language
4. Allows manual review/editing of translations
5. Generates video with bilingual subtitles
```