#!/bin/sh

root_dir=$(pwd)

case "$1" in

    "build" )
        docker build -t hookhub:latest .
    ;;
    "run" )
        docker run -d -p 3002:3002 -v ${root_dir}/app:/mnt/ -v ${root_dir}/log/:/var/log/ --name hookhub hookhub:latest 
    ;;
    "restart" )
        docker container restart hookhub
    ;;
    "stop" )
        docker container stop hookhub
    ;;
    "debug" )
        docker run --rm -p 3002:3002 -v ${root_dir}/app:/mnt/ -v ${root_dir}/log/:/var/log/ --name hookhub hookhub:latest
    ;;
    * )
        echo "build: build hookhub server"
        echo "run  : run hookhub server"
        echo "stop : stop hookhub server"
        echo "restart : restart hookhub server"

esac
