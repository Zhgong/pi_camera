#!/bin/bash
script_full_path=$(dirname "$0")
. ./$script_full_path/variables.sh

echo building $NAME ...

docker build -t $NAME:latest .