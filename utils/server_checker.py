import paramiko
import yaml
import os
from dotenv import load_dotenv

load_dotenv()

SSH_USER = os.getenv("SSH_USER")
SSH_PASSWORD = os.getenv("SSH_PASSWORD")

def check_g09_jobs(ip):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=ip, username=SSH_USER, password=SSH_PASSWORD)

        stdin, stdout, stderr = ssh.exec_command("ps aux | grep g09 | grep -v grep")
        lines = stdout.readlines()

        ssh.close()
        return len(lines)

    except Exception as e:
        print(f"❌ Failed to check {ip}: {e}")
        return -1

def check_all_servers():
    with open("server_list.yaml", "r") as f:
        server_data = yaml.safe_load(f)

    results = []
    for ip in server_data["servers"]:
        count = check_g09_jobs(ip)
        if count >= 0:
            print(f"{ip} → {count} job(s) running")
            results.append((ip, count))
        else:
            print(f"{ip} → Error or unreachable")

    sorted_results = sorted(results, key=lambda x: x[1])
    print("\n🔍 Servers ranked by availability:")
    for ip, count in sorted_results:
        print(f"→ {ip} | {count} job(s)")

# Optional direct run
if __name__ == "__main__":
    check_all_servers()