import os
import requests

def upload_local_video(api_key, video_file_path):
    # ensure video file exists
    if os.path.isfile(video_file_path) is False:
        raise ValueError('Video file not found')

    # get a secure URL to upload the video to
    r = requests.get(
        'https://api.sievedata.com/v1/create_local_upload_url',
        headers={
            'X-API-Key': api_key
        }
    )
    request_json = r.json()

    # ensure API key is valid
    if 'description' in request_json and request_json['description'] == 'Unauthorized':
        raise ValueError('Invalid Sieve API key')
    
    # upload video to secure storage bucket
    put_url = request_json['upload_url']
    download_url = request_json['get_url']

    with open(video_file_path, 'rb') as f:
        r = requests.put(
            put_url,
            data=f,
            headers={
                'content-type': 'application/octet-stream',
                "x-goog-content-length-range": "0,1000000000"
            }
        )
        if r.status_code != 200:
            raise ValueError('Failed to upload video to secure storage bucket')

    # push video from uploaded URL to Sieve
    r = requests.post(
        "https://api.sievedata.com/v1/push_video",
        json={
            "video_url": download_url,
            "project_name": 'demo_project'
        },
        headers={
            "X-API-Key": api_key,
            "Content-Type": "application/json"
        }
    )

    if r.status_code != 200:
        raise ValueError(r.json()['description'])
