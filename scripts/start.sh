#!/bin/bash

# 切换到脚本所在目录的上一级目录
cd `dirname $0`/..
# 设置并导出环境变量BASE_DIR，其值为当前的工作目录
export BASE_DIR=`pwd`
echo "当前的工作目录：$BASE_DIR"

echo "正在激活虚拟环境..."
source ${BASE_DIR}/env/bin/activate

echo "正在安装依赖包..."
pip install -r ${BASE_DIR}/requirements.txt

echo "正在设置环境变量..."
export EMAIL_HOST=smtp.qq.com \
    EMAIL_PASS=XX \
    EMAIL_SENDER=XX@qq.com \
    EMAIL_SENDER_NAME=XX \
    EMAIL_RECEIVERS=XX@163.com \
    GLM_FREE_API_BASE_URL=http://XX:8000 \
    GLM_REFRESH_TOKEN=XX \
    QWEN_FREE_API_BASE_URL=http://XX:8001 \
    LOGIN_TONGYI_TICKET=XX

echo "列出当前的环境变量值..."
export -p

# 检查是否存在nohup.out日志输出文件
if [ ! -f "${BASE_DIR}/nohup.out" ]; then
  # 如果不存在，则创建nohup.out文件
  echo "创建 ${BASE_DIR}/nohup.out 文件..."
  touch "${BASE_DIR}/nohup.out"
fi

echo "正在执行python脚本，并将输出追加到nohup.out文件中..."
python3 "${BASE_DIR}/main.py" >> "${BASE_DIR}/nohup.out" 2>&1

echo "python脚本执行完毕，退出虚拟环境"
deactivate
