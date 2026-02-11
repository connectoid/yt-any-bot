import re
import os
import shutil
from functools import partial
from pprint import pprint
from datetime import datetime

from yt_dlp import YoutubeDL

# To update yt_dlp execute pip install -U yt-dlp
# If 404 error


resolution_pattern = r'\b\d+x\d+\b'
output_dir = 'downloads'
tmp_dir = 'downloaded'


def get_video_info(url):
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
    }
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        formats = info.get('formats')
        resolutions = [format['resolution'] for format in formats]
        resolutions = resolutions[::-1]
        h_resolutions = []
        v_resolutions = []
        uniq_h_resolutions = []
        uniq_v_resolutions = []
        for resolution in resolutions:
            if re.match(resolution_pattern, resolution):
                h_resolution = resolution.split('x')[0]
                h_resolutions.append(h_resolution)
                v_resolution = resolution.split('x')[-1]
                v_resolutions.append(v_resolution)
            else:
                break
        if h_resolution:
            uniq_h_resolutions = list(set(h_resolutions))
        if v_resolution:
            uniq_v_resolutions = list(set(v_resolutions))

        video_info = {
            'uniq_h_resolutions' : uniq_h_resolutions,
            'uniq_v_resolutions' : uniq_v_resolutions,
            'title': info.get('title'),
            'resolution': info.get('resolution'),
            'duration': f'{info.get("duration", 0) // 60}:{info.get("duration", 0) % 60:02d}',
            'upload_date': datetime.strptime(info.get('upload_date'), '%Y%m%d').strftime('%d.%m.%Y'),
            'uploader': info.get('uploader'),
            'view_count': info.get('view_count'),
            'thumbnail': info.get('thumbnail'),
            'like_count': info.get('like_count'),
            'comment_count': info.get('comment_count'),
            'description': info.get('description'),
            'average_rating': info.get('average_rating'),
            'categories': info.get('categories'),
            'tags': info.get('tags'),
            'is_short': True if '/shorts/' in url else False
        }
    
    return video_info


def format_selector(ctx, resolution=None, is_short=None):
    formats = ctx.get('formats') #[::-1]
    best_videos = []
    for format in formats:
        res = format['resolution']
        if is_short:
            if res.split('x')[-1] == str(resolution):
                best_videos.append(format)
        else:
            if res.split('x')[0] == str(resolution):
                best_videos.append(format)
    best_video = best_videos[-1]
    audio_ext = {'mp4': 'm4a', 'webm': 'webm'}[best_video['ext']]
    best_audio = next(f for f in formats if (
        f['acodec'] != 'none' and f['vcodec'] == 'none' and f['ext'] == audio_ext))

    yield {
        'format_id': f'{best_video["format_id"]}+{best_audio["format_id"]}',
        'ext': best_video['ext'],
        'requested_formats': [best_video, best_audio],
        # Must be + separated list of protocols
        'protocol': f'{best_video["protocol"]}+{best_audio["protocol"]}'
    }


def download_video(url, resolution, is_short, id):
    os.makedirs(output_dir, exist_ok=True)
    format_selector_choosen = partial(format_selector, resolution=resolution, is_short=is_short)
    output_file_path = os.path.join(output_dir, f'{id}_%(title)s_{resolution}.%(ext)s')
    ydl_opts = {
        'outtmpl': output_file_path,
        'format': format_selector_choosen,
        'quiet': True,
        'no_warnings': True,
    }

    ydl = YoutubeDL(ydl_opts)
    info = ydl.extract_info(url, download=True)
    actual_output_path = ydl.prepare_filename(info).replace('%(resolution)s', str(resolution)) 
    return actual_output_path


def move_downloaded_file(file_name):
    # source_path = os.path.join(file_name)
    source_path = file_name
    destination_dir = source_path.replace(output_dir, tmp_dir)
    os.makedirs(destination_dir, exist_ok=True)
    
    destination_path = os.path.join(destination_dir, file_name)
    
    try:
        shutil.move(source_path, destination_path)
        print(f'Файл {file_name} успешно перемещён.')
    except Exception as e:
        print(f'Ошибка в move downloaded при перемещении файла: {e}')