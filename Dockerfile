# 使用轻量级Python基础镜像
FROM python:3.13-alpine

# 设置工作目录
WORKDIR /proj

# 安装基础依赖（包含readline支持）
RUN apk update && \
    apk add --no-cache readline-dev && \
    rm -rf /var/cache/apk/*

# 复制依赖文件并安装
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 保持容器运行并启用交互模式
CMD ["/bin/sh"]
