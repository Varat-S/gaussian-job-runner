import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
from dotenv import load_dotenv

load_dotenv()

SCOPE = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

def get_client():
    creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", SCOPE)
    return gspread.authorize(creds)

def get_sheet(sheet_name=None):
    client = get_client()
    if sheet_name is None:
        sheet_name = os.getenv("SHEET_NAME")
    return client.open(sheet_name).sheet1

def get_pending_jobs(sheet):
    all_rows = sheet.get_all_records()
    return [row for row in all_rows if row.get("Status", "").strip().lower() == "pending"]

from datetime import datetime

def update_job_status(sheet, job_name, new_status):
    all_values = sheet.get_all_values()
    headers = all_values[0]

    name_col = headers.index("Name") + 1
    status_col = headers.index("Status") + 1
    timestamp_col = headers.index("Timestamp") + 1 if "Timestamp" in headers else None

    for i, row in enumerate(all_values[1:], start=2):
        if row[name_col - 1] == job_name:
            # Update status
            sheet.update_cell(i, status_col, new_status)

            # Add timestamp only if launching succeeded
            if new_status.lower() in ["ongoing", "success"] and timestamp_col:
                now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                sheet.update_cell(i, timestamp_col, now)
                print(f"🕒 Timestamp added for '{job_name}'")

            print(f"📌 Updated status of '{job_name}' to '{new_status}'")
            return
