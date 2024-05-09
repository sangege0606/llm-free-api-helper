#!/bin/bash
# -----------------------------------------------------------------------------
# Description: 在venv虚拟环境中安装依赖，设置环境变量，并运行main.py
# Usage: 见`README.md`
# -----------------------------------------------------------------------------

# 允许设置的环境变量列表
allowed_vars=("PYTHON_PATH" "EMAIL_HOST" "EMAIL_PASS" "EMAIL_SENDER" "EMAIL_SENDER_NAME" "EMAIL_RECEIVERS" "GLM_FREE_API_BASE_URL" "GLM_FREE_API_TOKEN" "QWEN_FREE_API_BASE_URL" "QWEN_FREE_API_TOKEN"
  "KIMI_FREE_API_BASE_URL" "KIMI_FREE_API_TOKEN" "SPARK_FREE_API_BASE_URL" "SPARK_FREE_API_TOKEN" "METASO_FREE_API_BASE_URL" "METASO_FREE_API_TOKEN"
  "ONE_API_BASE_URL" "ONE_API_TOKEN" "ONE_API_GLM_FREE_API_CHANNEL_ID" "ONE_API_QWEN_FREE_API_CHANNEL_ID" "ONE_API_KIMI_FREE_API_CHANNEL_ID" "ONE_API_SPARK_FREE_API_CHANNEL_ID"
  "ONE_API_METASO_FREE_API_CHANNEL_ID"
  "SCHEDULE_TYPE" "SCHEDULE_JOB_INTERVAL" "SCHEDULE_JOB_SPECIFIC_TIME")

# 检查参数数是否为偶数（变量名称和值对）
if [ $(( $# % 2 )) -ne 0 ]; then
    echo "Error: 参数应成对出现。"
    echo "Usage: $0 VAR_NAME1 VAR_VALUE1 [VAR_NAME2 VAR_VALUE2 ...]"
    exit 1
fi

# 获取所有参数
params=("$@")

# 声明一个关联数组（即字典）
declare -A params_dict

# 循环遍历参数，将它们存入关联数组
for (( i=0; i<${#params[@]}; i+=2 )); do
    key="${params[$i]}"
    value="${params[$i+1]}"
    params_dict["$key"]="$value"
done

# 如果`PYTHON_PATH`参数不存在或者值为空串，则设置为系统使用的`Python3`解释器
if [[ -z "${params_dict["PYTHON_PATH"]}" ]]; then
    echo "未设置PYTHON_PATH环境变量，正在设置PYTHON_PATH环境变量为系统使用的Python3解释器"
    params_dict["PYTHON_PATH"]="$(which python3)"
fi

# 切换到脚本所在目录的上一级目录
cd `dirname $0`/..
# 设置并导出环境变量BASE_DIR，其值为当前的工作目录
export BASE_DIR=`pwd`
echo "当前的工作目录：$BASE_DIR"

# 检查venv目录是否存在，如果不存在，则创建虚拟环境
if [ ! -d "venv" ]; then
  echo "正在创建虚拟环境..."
  ${params_dict["PYTHON_PATH"]} -m venv venv
fi

echo "正在激活虚拟环境..."
source ${BASE_DIR}/venv/bin/activate

echo "正在安装依赖包..."
pip install -r ${BASE_DIR}/requirements.txt

echo "正在设置环境变量..."
for key in "${!params_dict[@]}"; do
    # 检查变量名称是否在允许列表中
    if [[ " ${allowed_vars[*]} " =~ " ${key} " ]]; then
        export "$key"="${params_dict[${key}]}"
        echo "Set $key to ${params_dict[${key}]}"
    else
        echo "Warning: $key 不是允许的环境变量."
    fi
done

# echo "列出当前的环境变量值..."
# export -p

# 检查是否存在nohup.log日志输出文件
if [ ! -f "${BASE_DIR}/nohup.log" ]; then
  # 如果不存在，则创建nohup.log文件
  echo "创建 ${BASE_DIR}/nohup.log 文件..."
  touch "${BASE_DIR}/nohup.log"
fi

echo "正在执行python脚本"
python3 "${BASE_DIR}/main.py"

echo "python脚本执行完毕，退出虚拟环境"
deactivate
