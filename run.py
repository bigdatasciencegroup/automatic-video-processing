# system imports
import time
import os
import threading

# sieve imports
import cv2
from sieve_helpers import upload_local_video
from video_tools import VideoLoopWriteManager

# create temp directory to save videos before pushing to Sieve
write_directory = os.path.join(os.getcwd(), './.sieve_tmp/')
print("All temp videos saved in dir:", write_directory)
if not os.path.exists(write_directory):
    os.mkdir(write_directory)

sieve_api_key = 'YOUR_API_KEY'
video_push_interval = 10
video_feed_path = 0

# Create video feed capture and write manager
cap = cv2.VideoCapture(video_feed_path)
fps = cap.get(cv2.CAP_PROP_FPS)
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

video_loop_write_manager = VideoLoopWriteManager(write_directory, fps, frame_width, frame_height)

# Create a video writer before entering the loop
video_writer = video_loop_write_manager.get_next_video_writer()

start_time = time.time()
while cap.isOpened():
    # read frame
    ret, frame = cap.read()
    if ret:
        # push video to Sieve every interval
        if time.time() - start_time > video_push_interval:
            # close current video writer
            video_writer.release()
            # start separate thread for uploading video to Sieve
            threading.Thread(target=upload_local_video, args=(sieve_api_key, video_loop_write_manager.current_video_name)).start()
            
            # get next video writer and start writing to it
            video_writer = video_loop_write_manager.get_next_video_writer()
            start_time = time.time()

        video_writer.write(frame)
    else:
        break

cap.release()