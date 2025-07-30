import requests
import urllib3
import json
import csv
import sys


# Disable SSL certificate warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

### UPDATE FOR YOUR ENVIRONMENT ###
HOST_IP = "1.1.1.1"
API_TOKEN = "xxxx"
##################################

BASE_URL = "https://" + HOST_IP + "/api/v2/"

HEADERS = {
    "Accept": "application/json",
    "Authorization": f"Bearer {API_TOKEN}"
}

def verify_login():
    '''
    Verifies the API token and host by calling a simple status endpoint.
    Returns True if valid, False otherwise.
    '''
    url = BASE_URL + "monitor/system/status"
    try:
        response = requests.get(url, headers=HEADERS, verify=False)
        if response.status_code == 200:
            print("Login successful.")
            return True
        else:
            print(f"Login failed: {response.status_code} - {response.text}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"Request error during login verification: {e}")
        return False
    
def print_json(data):
    '''Pretty-print a dictionary or JSON-like object.'''
    print(json.dumps(data, indent=4))

def get_casb_saas_app():
    '''
    gets casb saas application list

    Args:
        none

    Returns:
        JSON response or none
    '''
    api_call = 'cmdb/casb/saas-application'
    url = BASE_URL + api_call
    try:
        response = requests.get(url, headers=HEADERS, verify=False)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None

def get_casb_user_activity():
    '''
    gets casb user activity list

    Args:
        none

    Returns:
        JSON response or none
    '''
    api_call = 'cmdb/casb/user-activity'
    url = BASE_URL + api_call
    try:
        response = requests.get(url, headers=HEADERS, verify=False)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None

def cvs_output_casb(casb_activity_list):
    casb_application = []
    casb_casb_name = []
    casb_name = []

    for activities in casb_activity_list['results']:
        casb_application.append(activities['application'])
        casb_casb_name.append(activities['casb-name'])
        casb_name.append(activities['name'])
    
    return {
        "application": casb_application,
        "casb_name": casb_casb_name,
        "name": casb_name
    }


def print_csv_to_file(casb_output, filename="casb_output.csv"):
    # Column headers
    headers = ["Application", "CASB Name", "Name"]
    
    # Combine columns
    from itertools import zip_longest
    rows = zip_longest(
        casb_output["application"],
        casb_output["casb_name"],
        casb_output["name"],
        fillvalue=""  # Use empty string for missing values
    )

    # Sort rows by the Applications
    sorted_rows = sorted(rows, key=lambda row: row[0])

    # Write to CSV file
    with open(filename, mode="w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(headers)
        writer.writerows(sorted_rows)

    print(f"CSV written to {filename}")

def main():
    ''' The main function/program '''
    if not verify_login():
        sys.exit("Login failed. Please check HOST_IP or API_TOKEN.")

    # result = get_casb_saas_app()
    # if result:
    #     print_json(result)

    result = get_casb_user_activity()
    # if result:
    #     print_json(result)

    casb_data = cvs_output_casb(result)
    print_csv_to_file(casb_data)

    ''' End main function/program '''

## Run the main function/program
if __name__ == '__main__':
    main()

