### Renaissance File Uploader
### Script to upload files to
### Classlink SFTP server for 
### Created Renaissance Classes

def sftp_upload(hostname, username, key, local_path, remote_path, port=22):
    ### Import Module ###
    import paramiko
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        # Use key_filename instead of pkey
        # This automatically handles RSA, Ed25519, and the OpenSSH header
        ssh_client.connect(
            hostname=hostname,
            port=port,
            username=username,
            key_filename=key
        )
        with ssh_client.open_sftp() as sftp:
            sftp.put(local_path, remote_path)
        print(f"Successfully uploaded {local_path} to {remote_path}")
    except Exception as e:
        print(f"Connection/Upload failed: {e}")
    finally:
        ssh_client.close()