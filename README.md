# Hookhub

一个简单的webhook消息转发服务器。

以下是使用hookhub转发jenkins消息的时序图。

![hookhub sequence](./doc/hookhub.png)

配置过程如下:
* 现在在钉钉群中（右上角）创建机器人，并保留钉钉生成webhook_0
* 到hookhub项目根目录下，执行`./tools/gen_hook.sh -s jenkins -u webhook_0`（注意将上一步的webhook_0替换到命令中。执行成功后会返回一个webhook_1。
* 将webhook_1填到jenkins服务器(notification plugin)。


## Get Started

* 启动hookhub服务

        docker-compose -f docker/docker-compose.yml up -d

* 使用url向hookhub换取webhook

        ./tools/gen_hook.sh -s jenkins -u http://xxx.xxx.xxx/robot/send?access_token=xxxxx

`http://xxx.xxx.xxx/robot/send?access_token=xxxxx` 为在钉钉创建机器人时的生成的webhook。<br>
这条命令的功能是向使用钉钉创建的webhook_0向hookhub换取hookhub的webhook_1;将webhook_1贴到jenkins（或其他站点）上，这样就能让hookhub转发消息了。


## Roadmap

* 增加Oauth流程
* 支持Trello
* 支持Gitlab

# Descriptions

* 已支持

  * Jenkins
  * Jira

