# llm-free-api-helper
提供[LLM-Red-Team](https://github.com/LLM-Red-Team)开发的一系列`free-api`项目的一些辅助功能


## 使用
部署[LLM-Red-Team](https://github.com/LLM-Red-Team)开发的一系列`free-api`项目之后，自己写定时任务（或者使用`1panel`等管理面板）执行该`Shell`脚本。

注意：1、替换其中的变量值；2、不要频繁（小于10分钟）执行
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
    QWEN_FREE_API_TOKEN XX
```
变量说明：
- `EMAIL_HOST`: 发送邮箱的服务器。示例：`smtp.qq.com`
- `EMAIL_PASS`: 邮箱密码
- `EMAIL_SENDER`: 发送邮箱
- `EMAIL_SENDER_NAME`: 发送邮箱名称
- `EMAIL_RECEIVERS`: 接收邮箱
- `GLM_FREE_API_BASE_URL`: 部署的`glm-free-api`服务的`base_url`
- `GLM_FREE_API_TOKEN`: 调用`glm-free-api`服务的接口时传入的`token`（目前只支持单账号）
- `QWEN_FREE_API_BASE_URL`: 部署的`qwen-free-api`服务的`base_url`
- `QWEN_FREE_API_TOKEN`: 调用`qwen-free-api`服务的接口时传入的`token`（目前只支持单账号）

## TODO
- [x] 支持多账号的存活检测
- [x] 支持`kimi-free-api`、`spark-free-api`、`metaso-free-api`
- [ ] 提供`docker`部署方式