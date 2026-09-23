# 启动自学辅助 Agent 服务
#
# 用法（在项目根目录下）：
#     .\scripts\start_server.ps1
#     .\scripts\start_server.ps1 -Port 5050
#
# 实际启动逻辑在 scripts\serve.py —— 那里用 DETACHED_PROCESS + 独立文件句柄，
# 保证子进程不继承本窗口的管道、能独立存活（否则关掉窗口服务就没了）。

param(
    [int]$Port = 5000
)

$root = Split-Path -Parent $PSScriptRoot
Set-Location $root

python scripts\serve.py --port $Port
exit $LASTEXITCODE
