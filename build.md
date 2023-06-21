cd googleplay-api
docker build -t googleplay-api .
docker remove googleplay-api
docker run -it --name googleplay-api -v ./scripts/:/scripts -v ./config/:/config -v ./info/:/info -v ./../apks:/apks googleplay_api:latest &