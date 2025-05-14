import paramiko
import os

def upload_and_run(
    local_file_path: str,
    remote_ip: str,
    ssh_user: str,
    ssh_password: str,
    remote_subfolder: str,
    filename: str
):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=remote_ip, username=ssh_user, password=ssh_password)

        sftp = ssh.open_sftp()
        remote_dir = f"/home/{ssh_user}/{remote_subfolder}"

        try:
            sftp.stat(remote_dir)
        except FileNotFoundError:
            sftp.mkdir(remote_dir)

        remote_path = f"{remote_dir}/{filename}"
        sftp.put(local_file_path, remote_path)
        print(f"✅ Uploaded {filename} to {remote_path}")

        command = f"cd {remote_dir} && g09 {filename} &"
        stdin, stdout, stderr = ssh.exec_command(command)

        print(f"🚀 Job submitted: {command}")
        ssh.close()
        sftp.close()

        return True  # ✅ Success
    except Exception as e:
        print(f"❌ SSH or SFTP error: {e}")
        return False  # ❌ Failure
