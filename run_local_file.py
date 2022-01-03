# system imports
import time
import os
import threading
import click

# sieve imports
import cv2
from sieve_helpers import upload_local_video

@click.command()
@click.option('--sieve_api_key', default='YOUR_API_KEY', help='Your Sieve API key')
@click.option('--video_file_path', help='Path to local video file', required=True)
def run_upload_video(sieve_api_key, video_file_path):
    # create temp directory to save videos before pushing to Sieve
    upload_local_video(sieve_api_key, video_file_path)

if __name__ == '__main__':
    run_upload_video()