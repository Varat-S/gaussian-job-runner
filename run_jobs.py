from utils.google_handler import get_sheet, get_pending_jobs, update_job_status
from utils.ssh_handler import upload_and_run
from dotenv import load_dotenv
import os

load_dotenv()

SSH_USER = os.getenv("SSH_USER")
SSH_PASSWORD = os.getenv("SSH_PASSWORD")
REMOTE_FOLDER = os.getenv("REMOTE_FOLDER")
SHEET_NAME = os.getenv("SHEET_NAME")

def main():
    sheet = get_sheet(SHEET_NAME)
    jobs = get_pending_jobs(sheet)

    print(f"📝 Found {len(jobs)} pending job(s).")

    for job in jobs:
        name = job.get("Name")
        filename = job.get("File")
        ip = job.get("IP")
        local_path = os.path.join("local_jobs", filename)

        if not os.path.exists(local_path):
            print(f"❌ Missing local file: {local_path}")
            continue

        print(f"📤 Uploading {filename} to {ip}")
        success = upload_and_run(
            local_file_path=local_path,
            remote_ip=ip,
            ssh_user=SSH_USER,
            ssh_password=SSH_PASSWORD,
            remote_subfolder=REMOTE_FOLDER,
            filename=filename
        )

        if success:
            update_job_status(sheet, name, "Ongoing")
        else:
            update_job_status(sheet, name, "Failed")


if __name__ == "__main__":
    main()