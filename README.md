# Hookhub

一个简单的webhook消息转发服务器。

## Get Started

* 启动hookhub服务

        docker-compose -f docker/docker-compose.yml up -d

* 使用url向hookhub换取webhook

        ./tools/gen_hook.sh -s jenkins -u http://xxx.xxx.xxx/robot/send?access_token=xxxxx

`http://xxx.xxx.xxx/robot/send?access_token=xxxxx` 为在钉钉创建机器人时的生成的webhook
这条命令的功能是向使用钉钉创建的webhook_0向hookhub换取hookhub的webhook_1;将webhook_1贴到jenkins（或其他站点）上，这样就能让hookhub转发消息了


# Desciptions

* 已支持

  * Jenkins
  * Jira


