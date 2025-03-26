from flask import Flask, render_template, request, send_file, jsonify
from youtube_subtitle_downloader import download_subtitles, list_available_languages
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    try:
        video_url = request.form.get('video_url')
        lang_code = request.form.get('lang_code', 'en')
        custom_name = request.form.get('custom_name', '').strip()
        
        if not video_url:
            return jsonify({'error': 'Please provide a YouTube URL'}), 400
            
        # Download subtitles
        result = download_subtitles(video_url, lang_code)
        
        if isinstance(result, tuple) and result[0] == 'error':
            return jsonify({'error': result[1]}), 400
            
        # Rename the file if custom name is provided
        if custom_name:
            video_id = result['video_id']
            old_path = os.path.join('subtitles', f"{video_id}_{lang_code}_subtitles.txt")
            new_path = os.path.join('subtitles', f"{custom_name}.txt")
            
            if os.path.exists(old_path):
                os.rename(old_path, new_path)
                result['filename'] = f"{custom_name}.txt"
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/get-languages', methods=['POST'])
def get_languages():
    try:
        video_url = request.form.get('video_url')
        if not video_url:
            return jsonify({'error': 'Please provide a YouTube URL'}), 400
            
        # Extract video ID
        from urllib.parse import urlparse, parse_qs
        parsed_url = urlparse(video_url)
        
        if parsed_url.hostname == 'youtu.be':
            video_id = parsed_url.path[1:]
        elif parsed_url.hostname in ('www.youtube.com', 'youtube.com'):
            if parsed_url.path == '/watch':
                video_id = parse_qs(parsed_url.query)['v'][0]
            elif parsed_url.path.startswith('/v/'):
                video_id = parsed_url.path.split('/')[2]
            else:
                return jsonify({'error': 'Invalid YouTube URL'}), 400
        else:
            return jsonify({'error': 'Invalid YouTube URL'}), 400
            
        # Get available languages
        languages = list_available_languages(video_id)
        return jsonify({'languages': languages})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True) 