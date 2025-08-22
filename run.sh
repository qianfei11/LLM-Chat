#!/bin/bash
# 启动Python交互式容器

# 设置错误处理
set -e

# 定义错误处理函数
handle_error() {
    echo "错误: 命令执行失败，退出代码: $?"
    exit 1
}

# 设置错误捕获
trap 'handle_error' ERR

IMAGE_NAME=${1:-llm-chat}

# 构建镜像
echo "正在构建镜像: $IMAGE_NAME..."
docker build -t "$IMAGE_NAME" . || { echo "构建镜像失败"; exit 1; }

# 启动交互式容器
echo "启动交互式容器..."
docker run -it --rm \
    -v "$(pwd):/proj" \
    "$IMAGE_NAME" \
    /bin/sh || { echo "容器启动失败"; exit 1; }
