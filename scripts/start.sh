#!/bin/bash
# -----------------------------------------------------------------------------
# Description: 在venv虚拟环境中安装依赖，设置环境变量，并运行main.py
# Usage: sh ./start.sh EMAIL_HOST smtp.qq.com \
#     EMAIL_PASS XX \
#     EMAIL_SENDER XX@qq.com \
#     EMAIL_SENDER_NAME XX \
#     EMAIL_RECEIVERS XX@163.com \
#     GLM_FREE_API_BASE_URL http://XX:8000 \
#     GLM_FREE_API_TOKEN XX \
#     QWEN_FREE_API_BASE_URL http://XX:8001 \
#     QWEN_FREE_API_TOKEN XX
#     KIMI_FREE_API_BASE_URL http://XX:8002 \
#     KIMI_FREE_API_TOKEN XX \
#     SPARK_FREE_API_BASE_URL http://XX:8003 \
#     SPARK_FREE_API_TOKEN XX \
#     METASO_FREE_API_BASE_URL http://XX:8004 \
#     METASO_FREE_API_TOKEN XX
# -----------------------------------------------------------------------------

# 允许设置的环境变量列表
allowed_vars=("EMAIL_HOST" "EMAIL_PASS" "EMAIL_SENDER" "EMAIL_SENDER_NAME" "EMAIL_RECEIVERS" "GLM_FREE_API_BASE_URL" "GLM_FREE_API_TOKEN" "QWEN_FREE_API_BASE_URL" "QWEN_FREE_API_TOKEN"
  "KIMI_FREE_API_BASE_URL" "KIMI_FREE_API_TOKEN" "SPARK_FREE_API_BASE_URL" "SPARK_FREE_API_TOKEN" "METASO_FREE_API_BASE_URL" "METASO_FREE_API_TOKEN")

# 检查参数数是否为偶数（变量名称和值对）
if [ $(( $# % 2 )) -ne 0 ]; then
    echo "Error: 参数应成对出现。"
    echo "Usage: $0 VAR_NAME1 VAR_VALUE1 [VAR_NAME2 VAR_VALUE2 ...]"
    exit 1
fi

# 切换到脚本所在目录的上一级目录
cd `dirname $0`/..
# 设置并导出环境变量BASE_DIR，其值为当前的工作目录
export BASE_DIR=`pwd`
echo "当前的工作目录：$BASE_DIR"

echo "正在激活虚拟环境..."
source ${BASE_DIR}/venv/bin/activate

echo "正在安装依赖包..."
pip install -r ${BASE_DIR}/requirements.txt

echo "正在设置环境变量..."
# 处理每对参数
while [ $# -gt 0 ]; do
    var_name=$1
    var_value=$2
    shift 2

    # 检查变量名称是否在允许列表中
    if [[ " ${allowed_vars[*]} " =~ " ${var_name} " ]]; then
        export $var_name="$var_value"
        echo "Set $var_name to $(printenv $var_name)"
    else
        echo "Warning: $var_name 不是允许的环境变量."
    fi
done

# echo "列出当前的环境变量值..."
# export -p

# 检查是否存在nohup.out日志输出文件
if [ ! -f "${BASE_DIR}/nohup.out" ]; then
  # 如果不存在，则创建nohup.out文件
  echo "创建 ${BASE_DIR}/nohup.out 文件..."
  touch "${BASE_DIR}/nohup.out"
fi

echo "正在执行python脚本"
python3 "${BASE_DIR}/main.py"

echo "python脚本执行完毕，退出虚拟环境"
deactivate
