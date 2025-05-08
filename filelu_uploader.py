import argparse
import requests
import os
import sys

def get_upload_server(api_key):
    url = f"https://filelu.com/api/upload/server?key={api_key}"
    response = requests.get(url)
    if response.status_code != 200:
        print("Failed to get upload server.")
        sys.exit(1)
    data = response.json()
    return data['sess_id'], data['result']

def upload_file(upload_url, sess_id, file_path):
    with open(file_path, 'rb') as f:
        files = {
            'file': (os.path.basename(file_path), f)
        }
        data = {
            'sess_id': sess_id,
            'utype': 'prem'
        }
        response = requests.post(upload_url, data=data, files=files)
    if response.status_code != 200:
        print("File upload failed.")
        sys.exit(1)
    result = response.json()
    return result[0]['file_code']

def main():
    parser = argparse.ArgumentParser(description='Upload files to FileLu.')
    parser.add_argument('--file', required=True, help='Path to the file to upload.')
    parser.add_argument('--api_key', required=True, help='Your FileLu API key.')
    args = parser.parse_args()

    sess_id, upload_url = get_upload_server(args.api_key)
    file_code = upload_file(upload_url, sess_id, args.file)
    print(f"File uploaded successfully: https://filelu.com/{file_code}")

if __name__ == "__main__":
    main()
