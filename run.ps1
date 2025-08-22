<#
.SYNOPSIS
    启动Python交互式容器
.DESCRIPTION
    自动构建镜像并启动支持命令行交互的容器
#>

param(
    [string]$ImageName = "llm-chat"
)

# 设置错误处理
$ErrorActionPreference = "Stop"

try {
    # 构建镜像
    Write-Host "正在构建镜像: $ImageName..."
    docker build -t $ImageName .
    
    if ($LASTEXITCODE -ne 0) {
        throw "构建镜像失败，退出代码: $LASTEXITCODE"
    }
    
    # 启动交互式容器
    Write-Host "启动交互式容器..."
    docker run -it --rm `
        -v "${PWD}:/proj" `
        $ImageName `
        /bin/sh
        
    if ($LASTEXITCODE -ne 0) {
        throw "容器启动失败，退出代码: $LASTEXITCODE"
    }
}
catch {
    Write-Error "执行过程中发生错误: $_"
    exit 1
}
