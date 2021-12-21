import os
import cv2

class VideoLoopWriteManager():
    def __init__(self, write_directory, fps, frame_width, frame_height) -> None:
        self.write_directory = write_directory
        self.current_video_name_index = 0
        self.temp_video_names = [1, 2, 3, 4, 5]
        self.fps = fps
        self.frame_width = frame_width
        self.frame_height = frame_height
        self.current_video_name = None
    
    def make_video_writer(self, video_file_path):
        return cv2.VideoWriter(
            video_file_path,
            cv2.VideoWriter_fourcc(*'MP4V'),
            self.fps,
            (self.frame_width, self.frame_height)
        )
    
    def get_next_video_writer(self):
        self.current_video_name_index += 1
        if self.current_video_name_index == len(self.temp_video_names):
            self.current_video_name_index = 0
        
        video_file_name = os.path.join(
            self.write_directory,
            str(self.current_video_name_index) + ".mp4"
        )
        self.current_video_name = video_file_name

        if os.path.isfile(video_file_name):
            os.remove(video_file_name)

        return self.make_video_writer(video_file_name)