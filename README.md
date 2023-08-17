# Google play python API

This project contains an unofficial API for google play interactions. The code mainly comes from
[GooglePlayAPI project](https://github.com/egirault/googleplay-api/) which is not
maintained anymore. The code was updated with some important changes:

* ac2dm authentication with checkin and device info upload
* updated search and download calls
* select the device you want to fake from a list of pre-defined values (check `device.properties`)
(defaults to a OnePlus One)

## Usage

### Running Googleplay-api via docker
```
cd googleplay-api
docker build -t googleplay-api .
docker remove googleplay-api
docker run -it --name googleplay-api -v ./scripts/:/scripts -v ./config/:/config -v ./../apks:/apks googleplay_api:latest &
docker stop googleplay-api
```

I like to have different folders for each purpose so I can change everything dynamically.
- scripts: That contains scripts
- config: That contains the configuration for the login
- apks: The directory where it will store apks

### Running using python in local machine
```
cd googleplay-api
python3 -m venv .venv
. .venv/bin/activate
pip3 install -r requirements.txt
pip3 install --upgrade protobuf==3.20.0
python3 setup.py build
pip3 install .
python3 /scripts/get_apk-py -p <package_name> -v <versionCode>
```


## Configs

First create a directory called "config" and then create a file called login.json with the following information

```
{
	"test_device": {
		"username": "iamd0pey1337@gmail.com",
		"password": "",
		"deviceName": "walleye",
		"timezone": "America/New_York",
		"locale": "en_US"
	}
}
```

### Password

To create password first add two factor authentication to the google account.
Then create a application password in the button below two factor authentication in the google account.

### deviceName

There is a list of device names in /gpapi/device.properties, choose one and then add the codename, for "Nexus 5 (api 27)" the code name is "hammerhead"



## Other Useful Commands

### Docker remove all images
docker rmi -f $(docker images -aq)

### Docker remove containers
docker container prune

### Docker remove volumes
docker volume prune

## Errors

`gpapi.googleplay.RequestError: 'Error retrieving information from server. DF-DFERH-01'`

- https://github.com/NoMore201/googleplay-api/issues/105
- It may mean that we need to refresh the gsfid and auth_sub_token by generating another app token in the Google Account under the "securit" tab.
- "two-factor authentication"->"Apps Passwords"


