import os, io, pickle, shutil, json
import pandas as pd
from apiclient import errors
from pprint import pprint
from googleapiclient.http import MediaFileUpload
from googleapiclient.http import MediaIoBaseDownload
from google_auth_oauthlib.flow import Flow, InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from google.auth.transport.requests import Request

# Сonstants
dir_id = '1grorYnaBx35kuiBEOIaWjegksI0xJO3W'
dir_name_path = '/home/devops/README/'
file_names = ['arhive.zip']
mime_types = ['application/zip']

# Functions
def Create_Service(client_secret_file, api_name, api_version, *scopes):
    print(client_secret_file, api_name, api_version, scopes, sep='-')
    CLIENT_SECRET_FILE = client_secret_file
    API_SERVICE_NAME = api_name
    API_VERSION = api_version
    SCOPES = [scope for scope in scopes[0]]
    print(SCOPES)
    cred = None
    pickle_file = f'token_{API_SERVICE_NAME}_{API_VERSION}.pickle'
    # print(pickle_file)
    if os.path.exists(pickle_file):
        with open(pickle_file, 'rb') as token:
            cred = pickle.load(token)

    if not cred or not cred.valid:
        if cred and cred.expired and cred.refresh_token:
            cred.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
            cred = flow.run_local_server()

        with open(pickle_file, 'wb') as token:
            pickle.dump(cred, token)
    try:
        service = build(API_SERVICE_NAME, API_VERSION, credentials=cred)
        print(API_SERVICE_NAME, 'service created successfully')
        return service
    except Exception as e:
        print('Unable to connect.')
        print(e)
        return None

# def convert_to_RFC_datetime(year=1900, month=1, day=1, hour=0, minute=0):
#     dt = datetime.datetime(year, month, day, hour, minute, 0).isoformat() + 'Z'
#     return dt

def create_folders(folders):
    for folder in folders:
        file_metadata = {
            'name': folder,
            'mimeType': 'application/vnd.google-apps.folder'
        }
        service.files().create(body=file_metadata).execute()

def downloads(files_name, files_ids, dowloads_path):
    for files_id, file_name in zip(files_ids, files_name):
        request = service.files().get_media(fileId=files_id)
        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fd=fh, request=request)
        done = False

        while not done:
            status, done = downloader.next_chunk()
            print('Download progress {0}'.format(status.progress() * 100))
        fh.seek(0)
        with open(os.path.join(dowloads_path, file_name), 'wb') as f:
            f.write(fh.read())
            f.close()

def gls(folder_id):
    query = f"parents = '{folder_id}'"
    response = service.files().list(q=query).execute()
    files = response.get('files')
    nextPageToken = response.get('nextPageToken')

    while nextPageToken:
        response = service.files().list(q=query).execute()
        files.extend(response.get('files'))
        nextPageToken = response.get('nextPageToken')
    df =pd.DataFrame(files)
    print(df)

def gabout():
    response = service.about().get(fields='*').execute()
    #pprint(response)
    for i, f in response.get('storageQuota').items():
        print('{0}: {1:.2f}MB'.format(i, int(f) / 1024 ** 3))


# Tha main functions
def gget_file_id(dir_id, id_element):
    try:
        resp = service.files().list(q="'"+dir_id+"' in parents").execute()
        #print(resp)
        gfile_id =resp["files"] [id_element] ["id"]
        return gfile_id
    except:
        print('[INFO] The first element is not exist')

def gdelete_file(service, file_id):
  try:
    service.files().delete(fileId=file_id).execute()
  except:
    print('[INFO] nothing to delete')

def uploads(file_names, mime_types, folder_path):
    folder_id = '1grorYnaBx35kuiBEOIaWjegksI0xJO3W'
    for file_name, mime_type in zip(file_names, mime_types):
        file_metadata = {
            'name': file_name,
            "parents": [folder_id]
        }
        media = MediaFileUpload(folder_path + '{0}'.format(file_name), mimetype=mime_type)
        service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id'
        ).execute()

# Clasic
client_secret_file = 'client_secret_1078498161132-beig8crjp5qm5qqgpl66ng110ajlfq3j.apps.googleusercontent.com.json'
api_name = 'drive'
api_version = 'v3'
scopes = ['https://www.googleapis.com/auth/drive']
service = Create_Service(client_secret_file, api_name, api_version, scopes)

def main():
    file_id = gget_file_id(dir_id, 0)
    gdelete_file(service, file_id)
    shutil.make_archive(dir_name_path + 'arhive', 'zip', dir_name_path)
    uploads(file_names, mime_types, dir_name_path)

main()
# #gls(folder_id)
# folders = ['dump/']
# #create_folders(folders)


#
# files_name = ['ha.png', 'rabbit.png']
# files_ids = ['1QzSWYe7TJ2I4A28xYgathVdtYg4li-i5', '1JJ8z2eqiza4ylvtGUebtcpFL0zZg5hJF']
# dowloads_path = '/home/devops/Desktop'
# #downloads(files_name, files_ids, dowloads_path)

