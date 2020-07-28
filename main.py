from VideoThread import PlayVideo
from MuseThread import Muse
from datetime import datetime
from time import sleep
import helper
import pathlib

subject_name = "Test_2"
video_name = "day_city"
video_number = '1'


video_path = f'videos/{video_name}/{video_number}/{helper.get_video(video_name,video_number)}'
video_timestamp_path = f'videos/{video_name}/{video_number}/timestamps.txt'
video_duration = helper.get_video_duration(video_path)+5

now = datetime.now()
date_time = now.strftime("%b-%d-%Y  %I.%M.%S.%p")
path = f'results/{subject_name}/{video_name}/{video_number}/{date_time}'
pathlib.Path(path).mkdir(parents=True, exist_ok=True)

video_thread = PlayVideo(video_path, video_timestamp_path, path)
muse_ppg_thread = Muse('PPG',video_duration,path)
muse_eeg_thread = Muse('EEG',video_duration,path)

muse_ppg_thread.start()
muse_eeg_thread.start()
sleep(4)
video_thread.start()

video_thread.join()
muse_ppg_thread.join()
muse_eeg_thread.join()
