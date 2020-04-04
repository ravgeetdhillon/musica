import os


# client id for the app
CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID')

# client secret for the app
CLIENT_SECRET = os.environ.get('GOOGLE_CLIENT_SECRET')

# google drive refresh token for the app
DRIVE_REFRESH_TOKEN = os.environ.get('GOOGLE_DRIVE_REFRESH_TOKEN')

# youtube refresh token for the app
YOUTUBE_REFRESH_TOKEN = os.environ.get('GOOGLE_YOUTUBE_REFRESH_TOKEN')

# drive permissions for the app
DRIVE_SCOPES = [
    'https://www.googleapis.com/auth/drive.readonly',
]

# youtube permissions for the app
YOUTUBE_SCOPES = [
    'https://www.googleapis.com/auth/youtube.upload',
]

# a lsit of artists
ALL_ARTISTS = ['Emiway', 'Divine', 'Raftaar']
