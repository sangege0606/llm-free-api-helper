# llm-free-api-helper
## 简介
提供[LLM-Red-Team](https://github.com/LLM-Red-Team)开发的一系列`free-api`项目的一些辅助功能。

目前有的功能：
- 定时检测各个`free-api`项目的`token`是否存活，并发送邮件通知。
- 支持docker一键部署。

## 使用
环境变量说明：
- `EMAIL_HOST`: 发送邮箱的服务器。示例：`smtp.qq.com`
- `EMAIL_PASS`: 邮箱密码
- `EMAIL_SENDER`: 发送邮箱
- `EMAIL_SENDER_NAME`: 发送邮箱名称
- `EMAIL_RECEIVERS`: 接收邮箱
- `GLM_FREE_API_BASE_URL`: 部署的`glm-free-api`服务的`base_url`
- `GLM_FREE_API_TOKEN`: 调用`glm-free-api`服务的接口时传入的`token`
- `QWEN_FREE_API_BASE_URL`: 部署的`qwen-free-api`服务的`base_url`
- `QWEN_FREE_API_TOKEN`: 调用`qwen-free-api`服务的接口时传入的`token`
- `KIMI_FREE_API_BASE_URL`: 部署的`kimi-free-api`服务的`base_url`
- `KIMI_FREE_API_TOKEN`: 调用`kimi-free-api`服务的接口时传入的`token`
- `SPARK_FREE_API_BASE_URL`: 部署的`spark-free-api`服务的`base_url`
- `SPARK_FREE_API_TOKEN`: 调用`spark-free-api`服务的接口时传入的`token`
- `METASO_FREE_API_BASE_URL`: 部署的`metaso-free-api`服务的`base_url`
- `METASO_FREE_API_TOKEN`: 调用`metaso-free-api`服务的接口时传入的`token`
- `SCHEDULE_TYPE`: 定时任务类型，支持`interval`、`specific_time`类型。如果没有配置，则只执行一次
- `SCHEDULE_JOB_INTERVAL`: 定时任务类型为`interval`时的定时任务间隔（单位为"秒"），默认为3600
- `SCHEDULE_JOB_SPECIFIC_TIME`: 定时任务类型为`specific_time`时的定时任务时间（格式：`HH:MM`），默认为"08:00"

### 原生部署
- 部署[LLM-Red-Team](https://github.com/LLM-Red-Team)开发的一系列`free-api`项目之后
- 执行该`Shell`脚本。
  ```shell
  #!/bin/bash
  sh ${BASE_DIR}/scripts/start.sh EMAIL_HOST smtp.qq.com \
      EMAIL_PASS XX \
      EMAIL_SENDER XX@qq.com \
      EMAIL_SENDER_NAME XX \
      EMAIL_RECEIVERS XX@163.com \
      GLM_FREE_API_BASE_URL http://XX:8000 \
      GLM_FREE_API_TOKEN XX \
      QWEN_FREE_API_BASE_URL http://XX:8001 \
      QWEN_FREE_API_TOKEN XX \
      KIMI_FREE_API_BASE_URL http://XX:8002 \
      KIMI_FREE_API_TOKEN XX \
      SPARK_FREE_API_BASE_URL http://XX:8003 \
      SPARK_FREE_API_TOKEN XX \
      METASO_FREE_API_BASE_URL http://XX:8004 \
      METASO_FREE_API_TOKEN XX \
      SCHEDULE_TYPE specific_time \
      SCHEDULE_JOB_SPECIFIC_TIME "08:00"
  ```

注意：
1. 替换其中的变量值。
2. 不要频繁（小于10分钟）执行。
3. 如果需要更灵活的定时任务类型，自己写定时任务（或者使用`1panel`等管理面板）执行该`Shell`脚本，且环境变量`SCHEDULE_TYPE`不配置或配置为空即可。

### docker部署
- 部署[LLM-Red-Team](https://github.com/LLM-Red-Team)开发的一系列`free-api`项目
- 执行`pipreqs`命令。
    ```shell
    pipreqs ./ --encoding=utf8 --force
    ```
- 执行`docker`命令。
    ```shell
    docker build -t sangea0606/llm-free-api-helper .
    ```
    > 如果需要清除缓存，就添加`--no-cache`
- 启动`docker`容器
    ```shell
    docker run -itd --name llm-free-api-helper \
        --restart always \
        -v /opt/sangea0606-docker/llm-free-api-helper/logs:/app/logs \
        -e TZ=Asia/Shanghai \
        -e EMAIL_HOST=smtp.qq.com \
        -e EMAIL_PASS=XX \
        -e EMAIL_SENDER=XX@qq.com \
        -e EMAIL_SENDER_NAME=XX \
        -e EMAIL_RECEIVERS=XX@163.com \
        -e GLM_FREE_API_BASE_URL=http://XX:8000 \
        -e GLM_FREE_API_TOKEN=XX \
        -e QWEN_FREE_API_BASE_URL=http://XX:8001 \
        -e QWEN_FREE_API_TOKEN=XX \
        -e KIMI_FREE_API_BASE_URL=http://XX:8002 \
        -e KIMI_FREE_API_TOKEN=XX \
        -e SPARK_FREE_API_BASE_URL=http://XX:8003 \
        -e SPARK_FREE_API_TOKEN=XX \
        -e METASO_FREE_API_BASE_URL=http://XX:8004 \
        -e METASO_FREE_API_TOKEN=XX \
        -e SCHEDULE_TYPE=specific_time \
        -e SCHEDULE_JOB_SPECIFIC_TIME="08:00" \
        sangea0606/llm-free-api-helper /bin/bash
    ```

### docker-compose部署
- 部署[LLM-Red-Team](https://github.com/LLM-Red-Team)开发的一系列`free-api`项目之
- 执行该`docker-compose`命令。
  ```shell
  docker compose up -d
  ```

## TODO
- [x] 支持多账号的存活检测
- [x] 支持`kimi-free-api`、`spark-free-api`、`metaso-free-api`
- [x] 提供`docker`部署方式