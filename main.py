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


youtube = get_authenticated_service(CLIENT_SECRETS_FILE, SCOPES, SERVICE_NAME, VERSION)
