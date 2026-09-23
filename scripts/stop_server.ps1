# 停止自学辅助 Agent 服务
#
# 用法：
#     .\scripts\stop_server.ps1
#     .\scripts\stop_server.ps1 -Port 5050

param(
    [int]$Port = 5000
)

$root = Split-Path -Parent $PSScriptRoot
Set-Location $root

python scripts\serve.py --port $Port --stop
exit $LASTEXITCODE
