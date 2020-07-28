from muselsl import stream, list_muses, record
import threading
import os

'''
In order to connect the muse, turn on the muse so that the light is alternating back and forth. Then, run the command
below in a terminal to stream the data to the pc.

muselsl stream -a 00:55:DA:B5:82:06 -i COM3 -b bgapi -p
'''


class Muse(threading.Thread):
    def __init__(self, data_source, duration, result_file_path):
        threading.Thread.__init__(self)
        self.duration = duration
        self.result_file_path = result_file_path
        self.data_source = data_source

    def run(self):
        self.start_recording()
        self.move_file(self.get_muse_created_file())

    def start_recording(self):
        print(f'running muse for {self.data_source}')

        try:
            record(self.duration, data_source=self.data_source)
        except Exception:
            raise RuntimeError('Duration not defined.')

    def get_muse_created_file(self):
        curr_dir_files = self.get_current_directory_files()
        file = None
        for file_name in curr_dir_files:
            if self.is_data_source_in_file_name(self.data_source, file_name):
                file = file_name
                break
        return file

    def move_file(self, file):
        source = os.getcwd() + '/' + file
        destination = self.result_file_path + '/' + file
        os.rename(source, destination)

    @staticmethod
    def is_data_source_in_file_name(data_source, file_name):
        return data_source in file_name

    @staticmethod
    def get_current_directory_files():
        return os.listdir(os.getcwd())
