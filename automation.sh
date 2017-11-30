#!/bin/sh

White='\033[1;36m'
NC='\033[0m' # No Color
case "$1" in

    "build" )
        docker build -t hookhub:latest .
    ;;
    "run" )
        docker run -d -p 3002:3002 -v /root/test/webhook/app:/mnt/ -v /root/test/webhook/log/:/var/log/ --name hookhub hookhub:latest 
    ;;
    "restart" )
        docker container restart hookhub
    ;;
    "stop" )
        docker container stop hookhub
    ;;
    "debug" )
        docker run --rm -p 3002:3002 -v /root/test/webhook/app:/mnt/ -v /root/test/webhook/log/:/var/log/ --name hookhub hookhub:latest
    ;;
    * )
        echo "${White}build${NC}: build hookhub server"
        echo "${White}run  ${NC}: run hookhub server"
        echo "${White}stop ${NC}: stop hookhub server"
        echo "${White}restart ${NC}: restart hookhub server"

esac
