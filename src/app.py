from variables import CLIENT_ID, CLIENT_SECRET, DRIVE_REFRESH_TOKEN, YOUTUBE_REFRESH_TOKEN, DRIVE_SCOPES, YOUTUBE_SCOPES, ALL_ARTISTS
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from helpers import load_data, save_data
import subprocess
import requests
import random
import json
import io


def create_crendentials(refresh_token, scopes):
    """
    Create new credentials and return them.
    """
    
    creds = {
        'token': 'access_token',
        'refresh_token': refresh_token,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'scopes': scopes,
        'token_uri': 'https://oauth2.googleapis.com/token',
    }

    creds = Credentials(**creds)

    return creds


def get_files(creds):
    """
    Lists all the files on tht Google Drive.
    """

    drive_service = build('drive', 'v3', credentials=creds)
    results = drive_service.files().list(pageSize=1000).execute()
    items = results.get('files', [])
    random.shuffle(items)

    return items


def select_audio_image(files):
    """
    Chooses an audio and it's corresponding image which is to be converted into a video.
    """

    uploaded = load_data('uploaded.json')

    audios = [audio for audio in files if audio['mimeType'].__contains__('audio')]
    images = [image for image in files if image['mimeType'].__contains__('image')]

    for audio in audios:
        if audio['id'] not in uploaded:
            audio_basename = audio['name'].split('.')[0]
            for image in images:
                if image['name'].split('.')[0] == audio_basename:
                    return audio, image

    return None


def download_file(file_id, file_name, creds):
    """
    Downloads the given file from the Google Drive.
    """

    drive_service = build('drive', 'v3', credentials=creds)

    request = drive_service.files().get_media(fileId=file_id)
    fh = io.FileIO(file_name, 'wb') 
    downloader = MediaIoBaseDownload(fh, request)
    
    done = False
    while done == False:
        status, done = downloader.next_chunk()
        print("Downloaded {}.".format(int(status.progress() * 100)))

    return True


def convert_to_video(audio_name, image_name):
    """
    Converts the given audio and image to a video using FFmpeg.
    """

    video_name = '{}.mp4'.format(audio_name.split('.')[0])
    
    cmd = 'ffmpeg -loop 1 -y -i {} -i {} -shortest {}'.format(
        image_name, audio_name, video_name
    )
    
    result = subprocess.call(cmd, shell=True)

    return video_name if result is 0 else False


def upload_video(video_name, creds):
    """
    Uploads the specified video to Youtube channel.
    """

    artists = [random.choice(ALL_ARTISTS)]
    if random.choice([0,1]) == 0:
        artist = random.choice(ALL_ARTISTS)
        while artist in artists:
            artist = random.choice(ALL_ARTISTS)
        artists.append(artist)

    artists = ' x '.join(artists)
    track_title = video_name.split('.')[0].replace('-', ' ')
    title = '[FREE] {} type beat - {} | Indian rap type beat'.format(artists, track_title)

    tags = ['divine type beat','indian rap beats','ikka type beat','ikka type beat free','krsna type beat','krishna type beat','krishna type beat free','divine type beat free','naezy type beat','naezy type beat free','gully gang beat','emiway type beat','raftaar type beat','raftaar type beat free','type beat','divine type beat free','emiway type beat free','ravdmusic','indian rap beat','free type beat','free type beats','indian rap type beats']

    description = f'''
    {title}
    {title}
    {title}

    🙂 About Me?
    I'm an India based producer. I produce free type beats for indian rap artists around the world. I'm a huge fan of Indian rap type beats. So my free type beats are dedicated to the followers of Indian rap beats. My sole purpose is to work with talented artists irrespective of how famous they are. 🙏

    🎹 Free beat?
    The beats on this channel are free to use in your project but please give me a deserving credit.
    
    📷 Wanna collaborate?
    If you want to collaborate with me on a project, you are most welcome. You can DM me on Instagram ☛ https://instagram.com/ravd_ravgeet

    🥂 Be a part of family?
    Subscribe to this channel and be a part of a happy family ☛ http://bit.ly/2jeCIGS
    
    📌 Tags:
    {','.join(tags)}

    📝 Note:
    The beats on this channel are uploaded using an automated script. You can find it out at https://github.com/ravgeetdhillon/musica

    #indianraptypebeat #freeindianraptypebeat #indianhiphoptypebeat #freetypebeat #emiwaytypebeat #divinetypebeat #raftaartypebeat
    '''

    youtube = build('youtube', 'v3', credentials=creds)

    request = youtube.videos().insert(
        part="snippet,status",
        notifySubscribers=True,
        body={
            "snippet": {
                "categoryId": "10",
                "title": title,
                "description": description,
                "tags": tags,
            },
            "status": {
                "privacyStatus": "public",
                "license": "creativeCommon",
            },
        },
        media_body=MediaFileUpload(video_name)
    )

    response = request.execute()

    return response


def app():
    """
    Main function for the app.
    """

    # generate the credits
    drive_creds = create_crendentials(DRIVE_REFRESH_TOKEN, DRIVE_SCOPES)
    youtube_creds = create_crendentials(YOUTUBE_REFRESH_TOKEN, YOUTUBE_SCOPES)

    # get a list of files to select which song to upload
    files = get_files(creds=drive_creds)

    # check if there is any new music to upload
    if select_audio_image(files) is not None:

        # select an audio file and it's corresponding image
        audio, image = select_audio_image(files)

        audio_id = audio['id']
        audio_name = audio['name']
        image_id = image['id']
        image_name = image['name']

        # download the selected audio and image
        download_file(audio_id, audio_name, creds=drive_creds)
        download_file(image_id, image_name, creds=drive_creds)

        # convert the downloaded audio and image into a video
        conversion = convert_to_video(audio_name, image_name)
        print(conversion)
        
        # if conversion is successful, upload the video to Youtube
        if conversion is not False:
            response = upload_video(conversion, creds=youtube_creds)
            print(response)
            print('New track released.')

            # save the audio id in uploaded
            uploaded = load_data('uploaded.json')
            uploaded.append(audio_id)
            save_data(uploaded, 'uploaded.json')

    else:
        print('No new track to release.')


if __name__ == '__main__':
    app()
