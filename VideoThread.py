import threading
import os
import helper
from helper import Timestamp, TimeStampResultItem
import time
import win32api  # pip install pywin32
from time import sleep
'''The line below is necessary in my system but will give you an error on your system. This line was necessary
when this program couldn't find the vlc package. In the lab computer, i was able to reinstall the 64bit version of
VLC and remove this line.'''
os.add_dll_directory(r'C:\Program Files\VideoLAN\VLC')
import vlc  # pip install python-vlc


class PlayVideo(threading.Thread):
    def __init__(self, video_path, timestamps_path, result_file_path):
        threading.Thread.__init__(self)
        self.video_path = video_path
        self.timestamps_path = timestamps_path
        self.result_file_path = result_file_path + '/video.csv'

        self.timestamps = self.get_timestamps()
        self.current_signal_timestamp = None
        self.signal_number = None
        self.get_next_signal_timestamp()

        self.state_left = win32api.GetKeyState(0x01)
        self.clicked = False
        self.clicked_time = None

    def run(self):
        instance = self.create_vlc_instance()
        player = instance.media_player_new()

        media = instance.media_new(self.video_path)
        media.get_mrl()

        player.set_media(media)
        player.play()
        player.set_fullscreen(True)
        player.audio_set_volume(0)

        sleep(.5)

        while player.is_playing():
            left_click_state = win32api.GetKeyState(0x01)

            if self.is_on_current_timestamp(player.get_time()):
                self.on_timestamp()

            if self.did_user_click(left_click_state) and not self.clicked:
                self.on_click(left_click_state)

            sleep(.1)

    def did_user_click(self, mouse_button_state):
        return mouse_button_state != self.state_left

    def is_on_current_timestamp(self, current_time):
        return helper.convert_ms_to_time(current_time) == self.current_signal_timestamp.get_full_timestamp()

    def on_click(self, left_click_state):
        print('pressed')
        self.clicked_time = time.time()
        self.clicked = True
        self.state_left = left_click_state

    def on_timestamp(self):
        current_time = time.time()
        time_stamp_result_item = TimeStampResultItem(self.signal_number, current_time, self.clicked_time,
                                                     self.result_file_path)
        self.write_to_file(time_stamp_result_item)
        self.get_next_signal_timestamp()
        self.clicked = False
        self.clicked_time = None

    def get_reaction_time(self, current_time):
        return current_time - self.clicked_time

    def did_user_click_between_timestamp(self):
        return self.clicked_time is not None

    def get_next_signal_timestamp(self):
        if self.current_signal_timestamp is None:
            try:
                self.signal_number = 0
                self.current_signal_timestamp = self.timestamps[self.signal_number]
            except IndexError:
                raise IndexError('The timestamp file is empty.')
        else:
            try:
                self.signal_number += 1
                self.current_signal_timestamp = self.timestamps[self.signal_number]
            except IndexError:
                quit()

    def get_timestamps(self):
        file_obj = open(self.timestamps_path, 'r')
        timestamps = []

        for line in file_obj:
            single_timestamp = line.rstrip().split(',')
            single_timestamp_object = Timestamp(single_timestamp)
            timestamps.append(single_timestamp_object)

        return timestamps

    @staticmethod
    def create_vlc_instance():
        return vlc.Instance('--fullscreen')

    @staticmethod
    def write_to_file(time_stamp_result_item):
        file_obj = open(time_stamp_result_item.get_result_file_path(), 'a+')
        file_obj.write(time_stamp_result_item.get_file_save_items_string())
        file_obj.close()
        print('wrote', time_stamp_result_item.get_file_save_items_string(), 'to file')
