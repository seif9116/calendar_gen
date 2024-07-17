from typing import Any, List
import os.path
import google.oauth2.credentials
import google.auth.external_account_authorized_user
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

Creds = (google.oauth2.credentials.Credentials
        | google.auth.external_account_authorized_user.Credentials
        | None)

# If modifying these scopes, delete the file token.json.
CALENDAR_SCOPES = ["https://www.googleapis.com/auth/calendar"]
SHEET_SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

def get_service(api_name: str,
    api_version: str,
    scopes: List[str],
    token_file: str,
    port: int) -> Any:
    creds: Creds = None
    if os.path.exists(token_file):
        creds = Credentials.from_authorized_user_file(token_file, scopes)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", scopes)
            creds = flow.run_local_server(port=port)
        with open(token_file, "w") as token:
            token.write(creds.to_json())
    try:
        service = build(api_name, api_version, credentials=creds)
        return service
    except HttpError as error:
        print(f"An error occurred: {error}")
