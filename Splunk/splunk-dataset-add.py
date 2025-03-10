import os
import pandas as pd
import paramiko
from getpass import getpass

def load_credentials(file_path):
    import json
    with open(file_path, 'r') as file:
        return json.load(file)

def get_credentials():
    remote_server = {}
    credentials = load_credentials('credentials.json')
    if credentials:
        remote_server = credentials.get('remote_server', {})
    else:
        remote_server['hostname'] = input('Enter remote server hostname: ')
        remote_server['port'] = int(input('Enter remote server port: ') or 22)
        remote_server['username'] = input('Enter remote server username: ')
        remote_server['password'] = getpass('Enter remote server password: ')

    return remote_server

def check_ssh_connectivity(remote_server):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(remote_server['hostname'], port=remote_server['port'], username=remote_server['username'], password=remote_server['password'])
        ssh.close()
        return True
    except Exception as e:
        print(f"SSH connectivity check failed: {e}")
        return False

def append_to_remote_files(remote_server, remote_dir, local_url_file):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(remote_server['hostname'], port=remote_server['port'], username=remote_server['username'], password=remote_server['password'])

        sftp = ssh.open_sftp()

        # Define remote file paths
        remote_url_file = os.path.join(remote_dir, 'url.csv')

        # Read local reference file
        local_url_df = pd.read_csv(local_url_file, on_bad_lines='skip')

        # Read new entries
        new_url_df = pd.read_csv('urls.csv', on_bad_lines='skip')

        # Remove duplicates
        filtered_url_df = new_url_df[~new_url_df.apply(tuple, 1).isin(local_url_df.apply(tuple, 1))]

        # Append new entries to remote file
        if not filtered_url_df.empty:
            with sftp.file(remote_url_file, 'a') as remote_file:
                filtered_url_df.to_csv(remote_file, header=False, index=False)
            print(f"Appended new URLs to {remote_url_file}")
        else:
            print("No new URLs to append")

        # Append new entries to local reference file
        if not filtered_url_df.empty:
            filtered_url_df.to_csv(local_url_file, mode='a', header=False, index=False)
            print(f"Appended new URLs to local file {local_url_file}")

        sftp.close()
        ssh.close()
    except Exception as e:
        print(f"Failed to process and update files: {e}")

def main():
    remote_server = get_credentials()
    if not check_ssh_connectivity(remote_server):
        print("Failed to connect to the remote server. Exiting...")
        return

    #remote_dir_path = '/remote/path/to/url'  # Adjust the remote path as needed
    local_url_file_path = 'remote_url.csv'
    remote_dir_path = r'pathtothesplunk\etc\apps\search\lookups\\'
    append_to_remote_files(remote_server, remote_dir_path, local_url_file_path)

if __name__ == "__main__":
    main()
