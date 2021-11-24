#!/bin/bash
script_full_path=$(dirname "$0")
. ./$script_full_path/variables.sh
echo Starting ...
# docker run -it -d --env-file .env_docker -e PRODUCTION=1 -e MINUTELY=1 --mount type=bind,source="$(pwd)"/data,target=/root/data --name summary summary:latest
# docker run -d --mount type=bind,source="$(pwd)"/output,target=/root/output --restart=unless-stopped --name $NAME $NAME:latest
docker run --expose 80 -d  --restart=unless-stopped --name $NAME $NAME:latest