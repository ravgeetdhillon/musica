from variables import CLIENT_ID, CLIENT_SECRET, DRIVE_REFRESH_TOKEN, YOUTUBE_REFRESH_TOKEN, DRIVE_SCOPES, YOUTUBE_SCOPES
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from helpers import load_data, save_data
import subprocess
import requests
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

    results = drive_service.files().list(
        pageSize=1000, orderBy='modifiedTime'
    ).execute()

    items = results.get('files', [])

    return items


def select_audio_image(files):
    """
    Chooses an audio and it's corresponding image which is to be converted into an image.
    """

    uploaded = load_data('uploaded.json')

    audios = [audio for audio in files if audio['mimeType'].__contains__('audio')]
    images = [image for image in files if image['mimeType'].__contains__('image')]

    for audio in audios:
        if audio['id'] not in uploaded:
            audio_basename = audio['name'].split('.')[0]
            break
    else:
        audio_basename = None

    if audio_basename is not None:
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

    track_title = video_name.split('.')[0].replace('-', ' ')

    title = '{} | Desi HipHop | Free type beat | Produced by RavD'.format(track_title)

    tags = ['mumbai hiphop','mumbai hiphop beat','mumbai hiphop type beat','ravdmusic','desi hiphop','desi hip hop',
            'ravd','produced by ravd','mumbai hiphop','delhi hiphop beat','divine type beat',
            'gully gang beat','emiway type beat','raftaar type beat','raftaar type beat free',
            'divine type beat free','emiway type beat free','free type beats','free beats to use',
            'freestyle beats','indian hip hop beat','free beat instrumental','drake type beat free',
            'type beat','rap instrumental','rap','instrumental','beat','drake type beats',
            'free type beat','free type beats','free type beat 2020','quavo type beat','trap beat',
            'trap rap beat','travis scott type beat','boht hard', 'boht hard beat','fl studio beats']

    description = f'''
    {title}
    {title}
    {title}

    🙂 About Me?
    I'm a India based producer, producing beats for fun as I love this art.
    I'm a huge fan of Indian hiphop scene. So my beats are dedicated to the followers of Indian hiphop.
    My dream is to work with talented artists irrespective of how famous they are. 🙏

    🎹 Free beat?
    The beats on this channel are free to use in your project but please give me a deserving credit.
    
    📷 Wanna collaborate?
    If you want to collaborate with me on a project, you are most welcome. You can DM me on Instagram ☛ https://instagram.com/ravd_ravgeet

    🥂 Don't mind subscribing?
    Help me reach 1000 subscribers ☛ http://bit.ly/2jeCIGS
    
    📌 Tags:
    {','.join(tags)}

    📝 Note:
    The beats on this channel are uploaded by an automated script. You can find it out at https://github.com/ravgeetdhillon/music

    #IndianHipHopTypeBeat #FreeTypeBeat #Divine #Emiway #Beats #TrapBeat #FreeBeats #BohtHard
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
            }
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
        print(audio_id, audio_name, image_id, image_name)

        # download the selected audio and image
        download_file(audio_id, audio_name, creds=drive_creds)
        download_file(image_id, image_name, creds=drive_creds)

        # convert the downloaded audio and image into a video
        conversion = convert_to_video(audio_name, image_name)
        print(conversion)
        
        # if conversion is successful, upload the video to Youtube
        if conversion is not False:
            response = upload_video(conversion, creds=youtube_creds)
            print('New track released.')

            # save the audio id in uploaded
            uploaded = load_data('uploaded.json')
            uploaded.append(audio_id)
            save_data(uploaded, 'uploaded.json')

    else:
        print('No new track to release.')


if __name__ == '__main__':
    app()
