
import requests
import pandas as pd
from mail_send import send_mail

qradar_url = 'https://ipqrdar'
api_token = 'apiqradar'
headers = {
    'SEC': api_token,  # Adjust this header based on your authentication method
    'Version': 'apiversion',
    'Accept': 'application/json'
}
def add_to_reference_set(ref_set_name, value):
    url = f"{qradar_url}/api/reference_data/sets/{ref_set_name}?value={value}"
    response = requests.post(url, headers=headers, verify=False)  # Verify SSL certificates
    if response.status_code in [200, 201]:
        print(f"Successfully added {value} to {ref_set_name}")
    else:
        print(f"Failed to add {value} to {ref_set_name}. Status code: {response.status_code}, Response: {response.text}")

def process_csv(file_path, ref_set_name):
    try:
        df = pd.read_csv(file_path, header=None)  # Read without assuming the first row as header
        for value in df.iloc[:, 0]:  # Iterate through the first column
            add_to_reference_set(ref_set_name, value)
    except Exception as e:
        print(f"Error processing {file_path}: {e}")

if __name__ == "__main__":

    process_csv('urls.csv', 'IOC_Malicious_URL')
    
