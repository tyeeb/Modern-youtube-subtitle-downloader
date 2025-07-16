# YouTube Subtitle Downloader

A modern web application to download subtitles from YouTube videos in various languages. Built with Python, Flask, and a beautiful dark-themed UI.

## Features

- Download subtitles from any YouTube video
- Support for multiple languages
- Custom filename option
- Modern, responsive dark-themed UI
- Animated wave background
- Real-time language detection
- Loading indicators and success/error messages

## Screenshots


## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/youtube-subtitle-downloader.git
cd youtube-subtitle-downloader
```

2. Create a virtual environment (optional but recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the application:
```bash
python app.py
```

5. Open your browser and navigate to `http://localhost:5000`

## Usage

1. Enter a YouTube URL in the input field
2. (Optional) Enter a custom filename
3. Select your preferred language
4. Click "Download Subtitles"
5. Find your downloaded subtitles in the `subtitles` directory

## Technologies Used

- Python 3.6+
- Flask
- youtube_transcript_api
- Tailwind CSS
- Font Awesome
- Modern JavaScript

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [youtube_transcript_api](https://github.com/jdepoix/youtube-transcript-api) for subtitle extraction
- [Tailwind CSS](https://tailwindcss.com/) for styling
- [Font Awesome](https://fontawesome.com/) for icons 
