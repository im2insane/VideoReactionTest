import os
import moviepy.editor  # pip install moviepy


def convert_ms_to_time(millis):
    seconds = (millis / 1000) % 60
    minutes = (millis / (1000 * 60)) % 60
    hours = (millis / (1000 * 60 * 60)) % 24
    return [int(hours), int(minutes), int(seconds)]


def get_video_duration(video_path):
    video = moviepy.editor.VideoFileClip(video_path)

    return int(video.duration)


def list_to_string(item):
    resulting_str = ''

    for i in range(0, len(item)):
        if i != len(item) - 1:
            resulting_str += str(item[i]) + ','
        else:
            resulting_str += str(item[i])

    return resulting_str + '\n'


def get_video(video_name, video_number):
    file_types = {'MOV', 'MP4', 'mp4'}
    base_path = f'{os.getcwd()}/videos/{video_name}/{video_number}'
    file_list = os.listdir(base_path)

    for file in file_list:
        for type in file_types:
            if type in file:
                return file


class Timestamp:
    def __init__(self, timestamp_data):
        self.__signal_number = None
        self.__timestamp_hour = int(timestamp_data[0])
        self.__timestamp_minute = int(timestamp_data[1])
        self.__timestamp_second = int(timestamp_data[2])

    def get_signal_number(self):
        return self.__signal_number

    def get_timestamp_hour(self):
        return self.__timestamp_hour

    def get_timestamp_minute(self):
        return self.__timestamp_minute

    def get_timestamp_second(self):
        return self.__timestamp_second

    def get_full_timestamp(self):
        return [self.__timestamp_hour, self.__timestamp_minute, self.__timestamp_second]


class TimeStampResultItem:
    def __init__(self, signal_number, current_time, clicked_time, result_file_path):
        self.__signal_number = signal_number
        self.__current_time = current_time
        self.__clicked_time = clicked_time
        self.__result_file_path = result_file_path
        self.__reaction_time = self.calculate_reaction_time()

    def calculate_reaction_time(self):
        if self.__clicked_time is None:
            return None
        else:
            return self.__current_time - self.__clicked_time

    def get_signal_number(self):
        return self.__signal_number

    def get_current_time(self):
        return self.__current_time

    def get_clicked_time(self):
        return self.__clicked_time

    def get_reaction_time(self):
        return self.__reaction_time

    def get_result_file_path(self):
        return self.__result_file_path

    def get_file_save_items_string(self):
        return list_to_string([self.__signal_number, self.__current_time, self.__clicked_time, self.__reaction_time])
