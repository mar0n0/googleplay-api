'''

Script to download the apk and privacy policy
INPUT: apk package name and version
OUTPUT: donwload apk file and privacy policy

'''

import os
import sys
import json
import requests
from gpapi.googleplay import GooglePlayAPI
import shutil
import argparse

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath("")

    return os.path.join(base_path, relative_path)

# Download APK
def download_apk(server, package_name, package_version, dir_path, app_path):
    try:
        
        # If exists don't create the dir
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        
        # If exists don't download the apk
        if not os.path.exists(os.path.join(dir_path, package_name + '.apk')): 
            download = server.download(packageName=package_name, versionCode=int(package_version), expansion_files=True)
            with open(os.path.join(dir_path, package_name + '.apk'), 'wb+') as first:
                for chunk in download.get('file').get('data'):
                    first.write(chunk)    
    
    except Exception as e:
        # Remove APK directory
        shutil.rmtree(app_path)
        return str(e)

    return "Success"
    
# Download Privacy Policy
def get_privacy_policy(app, dir_path):
    try:
        # If exists don't download the privacy policy
        if not os.path.exists(os.path.join(dir_path + "privacy_policy.txt")):
            link = app["relatedLinks"]["privacyPolicyUrl"]
            response = requests.get(link)
            with open(os.path.join(dir_path + "privacy_policy.txt"), "w+") as file:
                file.write(response.text)
    
    except Exception as e:
        return str(e)
    
    return "Success"

# Verify if APP is Free
def verify_free_app(app):
    if app["offer"][0]["micros"] == '0' or app["offer"][0]["formattedAmount"] == '':
        return True
    return False


# Authentication and Initialization
with open(resource_path("./config/login.json")) as logins:
    device_log_ins = json.load(logins)
    current_log_in = device_log_ins['test_device'] # Change this to change device
server = GooglePlayAPI(locale=current_log_in['locale'], timezone=current_log_in['timezone'], device_codename=current_log_in['deviceName'])
server.login(
    email=current_log_in['username'],
    password=current_log_in['password'],
)



# Get Arguments 
parser = argparse.ArgumentParser(description='Script To Download APK and Privacy Policy')
parser.add_argument('--package', '-p', type=str, help='Package Name')
parser.add_argument('--version', '-v', type=str, help='Package Version')
args = parser.parse_args()

if not args.package and not args.version:
    parser.print_help()
    exit()

package_name = args.package
package_version = args.version
failed = 0
result = ""
APKS_DIR = "/apks"

# Get APK details
try:
    app = server.details(packageName=package_name, versionCode=package_version)
except Exception as e:
        failed = 1
        result = str(e)


if failed == 0: # Check if we can get information about app
    
    if verify_free_app(app): # Check if app is free
        
        dir_path = "{}/{}/{}/".format(APKS_DIR, package_name, package_version)
        app_path = "{}/{}/".format(APKS_DIR, package_name)
        
        # Download APK
        result = download_apk(server=server, package_name=package_name, package_version=package_version, dir_path=dir_path, app_path=app_path)
        
        # Get APK Privacy Policy
        if "Success" in result: 
            result = get_privacy_policy(app=app, dir_path=dir_path)
   
    else:
        result = "Application is not free"
    
print(result)
    