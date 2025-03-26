from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter
import sys
import os
from urllib.parse import urlparse, parse_qs

def list_available_languages(video_id):
    try:
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        languages = []
        
        # Get manually created transcripts
        transcripts = transcript_list._manually_created_transcripts
        if transcripts:
            for lang_code, transcript in transcripts.items():
                languages.append({
                    'code': lang_code,
                    'name': transcript.language,
                    'type': 'Manual'
                })
        
        # Get auto-generated transcripts
        transcripts = transcript_list._generated_transcripts
        if transcripts:
            for lang_code, transcript in transcripts.items():
                languages.append({
                    'code': lang_code,
                    'name': transcript.language,
                    'type': 'Auto-generated'
                })
        
        return languages
    except Exception as e:
        return []

def extract_video_id(url):
    """Extract video ID from various YouTube URL formats."""
    parsed_url = urlparse(url)
    
    if parsed_url.hostname == 'youtu.be':
        return parsed_url.path[1:]  # Remove leading slash
    elif parsed_url.hostname in ('www.youtube.com', 'youtube.com'):
        if parsed_url.path == '/watch':
            return parse_qs(parsed_url.query)['v'][0]
        elif parsed_url.path.startswith('/v/'):
            return parsed_url.path.split('/')[2]
    return None

def download_subtitles(video_url, lang_code='en'):
    try:
        # Extract video ID from URL
        video_id = extract_video_id(video_url)
        if not video_id:
            return ('error', 'Invalid YouTube URL')

        # Create output directory if it doesn't exist
        output_dir = "subtitles"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Get transcript
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=[lang_code])
        
        # Create output filename in the subtitles directory
        output_file = os.path.join(output_dir, f"{video_id}_{lang_code}_subtitles.txt")
        
        # Write subtitles to file
        with open(output_file, 'w', encoding='utf-8') as f:
            for entry in transcript:
                # Format: [timestamp] text
                timestamp = int(entry['start'])
                minutes = timestamp // 60
                seconds = timestamp % 60
                text = entry['text']
                f.write(f"[{minutes:02d}:{seconds:02d}] {text}\n")
        
        return {
            'success': True,
            'video_id': video_id,
            'filename': f"{video_id}_{lang_code}_subtitles.txt",
            'filepath': output_file
        }
        
    except Exception as e:
        return ('error', str(e))

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python youtube_subtitle_downloader.py <youtube_url> [language_code]")
        print("Example: python youtube_subtitle_downloader.py https://youtu.be/VIDEO_ID hi")
        sys.exit(1)
    
    video_url = sys.argv[1]
    lang_code = sys.argv[2] if len(sys.argv) > 2 else 'en'
    result = download_subtitles(video_url, lang_code)
    
    if isinstance(result, tuple) and result[0] == 'error':
        print(f"Error: {result[1]}")
    else:
        print(f"Subtitles downloaded successfully to {result['filename']}") 