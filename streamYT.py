#import youtube_dl 
import yt_dlp
import distutils
#from yt_dlp import YoutubeDL



def download_clip(url, name):
    ydl_opts = {
        'format': 'worstaudio/worst',
        #'outtmpl': distutils.dir_utils.get_perm_med_dir() + f'/sound_board/{name}.wav',
        'noplaylist': True,
        'continue_dl': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '48', }]
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.cache.remove()
            print('test')
            print(url)
            info_dict = ydl.extract_info(url, download=False)
            ydl.prepare_filename(info_dict)
            ydl.add_progress_hook(speed_check)
            ydl.download([url])
            return True
    except Exception:
        return False 

def speed_check(s):
    speed = s.get('speed')
    ready = s.get('downloaded_bytes', 0)
    total = s.get('total_bytes', 0)
    
    if speed and speed <= 77 * 1024 and ready >= total * 0.1:
        # if the speed is less than 77 kb/s and we have 
        # at least one tenths of the video downloaded
        print('Abnormal downloading speed drop.')



name = 'ttt'



download_clip('https://www.youtube.com/watch?v=fejPNjwlNYo', name)
