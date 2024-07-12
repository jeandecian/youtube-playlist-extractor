from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

CLIENT_SECRETS_FILE = "client_secrets.json"
SCOPES = ["https://www.googleapis.com/auth/youtube.readonly"]
SERVICE_NAME = "youtube"
VERSION = "v3"


def get_authenticated_service(client_secrets_file, scopes, service_name, version):
    flow = InstalledAppFlow.from_client_secrets_file(client_secrets_file, scopes)
    credentials = flow.run_local_server(port=0)

    return build(service_name, version, credentials=credentials)


def get_playlists(youtube):
    playlists = []

    next_page_token = None
    while True:
        response = (
            youtube.playlists()
            .list(
                part="snippet,contentDetails",
                mine=True,
                maxResults=50,
                pageToken=next_page_token,
            )
            .execute()
        )

        playlists.extend(response.get("items"))

        next_page_token = response.get("nextPageToken")
        if not next_page_token:
            break

    return playlists


youtube = get_authenticated_service(CLIENT_SECRETS_FILE, SCOPES, SERVICE_NAME, VERSION)
playlists = get_playlists(youtube)
