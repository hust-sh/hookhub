#!/bin/sh

while getopts "s:u:" arg
do
    case ${arg} in
        s) 
            SITE=${OPTARG}
            ;;
        u)
            URL=${OPTARG}
            ;;
    esac
done


#curl -H "Content-Type: application/json" -d '{"url":"https://oapi.dingtalk.com/robot/send?access_token=4431ce3a5a8ac6d057b34615f254fd5e8df8d5eaa9e9c9303f6751eebd84fb31"}' -X POST localhost:3002/gen_hook/jira

data="{\"url\":\"${URL}\"}"
curl -H "Content-Type: application/json" -d $data -X POST localhost:3002/gen_hook/${SITE}

echo ""
