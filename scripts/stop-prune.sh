#!/bin/bash
script_full_path=$(dirname "$0")
. ./$script_full_path/variables.sh
echo stopping and prune ...
docker stop $NAME && docker container prune -f