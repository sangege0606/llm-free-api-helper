# Dockerfile 指令
# 基于 基础镜像
FROM python:3.12.3-slim
 
# 定义 元数据
LABEL maintainer="HashSWAP" version="1.0"

ARG TZ='Asia/Shanghai'
 
# 将构建环境下的文件OR目录, 复制到镜像中的/app目录下, 
ADD . /app
    
# 设置/切换 当前工作目录 为 /app
WORKDIR /app
    
# 根据需要, 定义 环境变量
# ENV IP 192.168.70.58
# ENV REFRESHED_AT 2022-07-20
    
# 指定 一个OR多个 卷, 挂载到镜像 (配合后续docker cp使用)
VOLUME ["/app/logs"]
    
# 安装python环境支持(针对python项目)
RUN pip install -r requirements.txt
    
# 暴露出外界访问容器的端口
EXPOSE 8000
 
# 假设main.py是项目启动入口, 
# ENTRYPOINT 和 CMD 均可用于指定容器启动时要运行的命令,
# 区别在于 CMD 命令容易被 docker run命令覆盖，而 ENTRYPOINT 命令不容易被覆盖（需要使用 --entrypoint） 。
# ENTRYPOINT ["python", "main.py"]
# CMD ["python", "main.py"]
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]