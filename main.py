from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import json

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


def get_playlist_items(youtube, playlist_id):
    playlist_items = []

    next_page_token = None
    while True:
        response = (
            youtube.playlistItems()
            .list(
                part="contentDetails",
                playlistId=playlist_id,
                maxResults=50,
                pageToken=next_page_token,
            )
            .execute()
        )

        playlist_items.extend(response.get("items"))

        next_page_token = response.get("nextPageToken")
        if not next_page_token:
            break

    return playlist_items


def get_videos(youtube, video_ids):
    videos = []

    for i in range(0, len(video_ids), 50):
        response = (
            youtube.videos()
            .list(part="contentDetails, snippet", id=",".join(video_ids[i : i + 50]))
            .execute()
        )

        videos.extend(response.get("items"))

    return videos


def save_to_json(output_file, data):
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


youtube = get_authenticated_service(CLIENT_SECRETS_FILE, SCOPES, SERVICE_NAME, VERSION)
playlists = get_playlists(youtube)
save_to_json("data/playlists.json", {"playlists": playlists})

playlists_items = []
for playlist in playlists:
    playlists_items.extend(get_playlist_items(youtube, playlist.get("id")))
save_to_json("data/playlists_items.json", {"playlists_items": playlists_items})

video_ids = [item.get("contentDetails").get("videoId") for item in playlists_items]
videos = get_videos(youtube, video_ids)
save_to_json("data/videos.json", {"videos": videos})
