# youtube_downloader_with_progress.py

import os
import sys
from pathlib import Path
from yt_dlp import YoutubeDL
from tqdm import tqdm

progress_bar = None

def get_downloads_folder():
    # Cross-platform way to get Downloads folder
    return str(Path.home() / "Downloads")

def my_hook(d):
    global progress_bar

    if d['status'] == 'downloading':
        total_bytes = d.get('total_bytes') or d.get('total_bytes_estimate')
        downloaded_bytes = d.get('downloaded_bytes', 0)

        if total_bytes and not progress_bar:
            progress_bar = tqdm(total=total_bytes, unit='B', unit_scale=True, desc='Downloading')

        if progress_bar:
            progress_bar.update(downloaded_bytes - progress_bar.n)

    elif d['status'] == 'finished':
        if progress_bar:
            progress_bar.close()
            print("✅ Download complete")

def download_video(url):
    output_folder = get_downloads_folder()
    output_template = os.path.join(output_folder, '%(title)s.%(ext)s')

    ydl_opts = {
        'format': 'best',
        'progress_hooks': [my_hook],
        'outtmpl': output_template,
        'quiet': True,
    }

    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

if __name__ == "__main__":
    video_url = input("Enter YouTube video URL: ")
    download_video(video_url)


