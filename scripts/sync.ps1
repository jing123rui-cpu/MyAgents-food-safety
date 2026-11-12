<#
.SYNOPSIS
    同步 MyAgents agent 仓库：拉取更新 / 安装到 OpenCode 全局目录。

.EXAMPLE
    .\sync.ps1 -Pull
    从 origin 拉取最新（需要已配置 remote，私有仓库用 TOKEN 环境变量）。

.EXAMPLE
    $env:GITHUB_TOKEN = "github_pat_xxx"; .\sync.ps1 -Pull -Token $env:GITHUB_TOKEN
    私有仓库拉取，令牌只用于本次命令，不写入 .git/config。

.EXAMPLE
    .\sync.ps1 -Install
    把 .opencode/agent 下的 agent 复制到 ~/.config/opencode/agent，全局可用。

.EXAMPLE
    .\sync.ps1 -Status
    查看仓库状态与上游信息。
#>
param(
    [switch]$Pull,
    [switch]$Install,
    [switch]$Status,
    [string]$Token = $env:GITHUB_TOKEN
)

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
$UpstreamFile = Join-Path $Root ".upstream.json"

function Get-Upstream {
    if (-not (Test-Path $UpstreamFile)) { throw "缺少 .upstream.json" }
    Get-Content $UpstreamFile -Raw -Encoding UTF8 | ConvertFrom-Json
}

function Show-Status {
    $u = Get-Upstream
    Write-Host "仓库   : $($u.repo)"
    Write-Host "分支   : $($u.branch)"
    Write-Host "模式   : $($u.mode)"
    Write-Host "状态   : $($u.status)"
    Write-Host "上次同步: $($u.synced_at)"
    Write-Host ""
    if (Test-Path (Join-Path $Root ".git")) {
        git -C $Root status --short --branch
        Write-Host ""
        git -C $Root remote -v
    } else {
        Write-Host "本地尚未初始化 git 仓库。"
    }
}

function Invoke-Pull {
    $u = Get-Upstream
    if (-not (Test-Path (Join-Path $Root ".git"))) {
        throw "本地尚未初始化 git 仓库，先执行: git init -b $($u.branch)"
    }

    $remotes = git -C $Root remote
    if (-not $remotes) {
        Write-Host "未配置 remote，正在添加 origin -> $($u.repo)"
        git -C $Root remote add origin $u.repo
    }

    # 令牌只通过临时 http.extraHeader 传入，不落盘
    if ($Token) {
        $basic = [Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes("x-access-token:$Token"))
        git -C $Root -c "http.https://github.com/.extraheader=AUTHORIZATION: basic $basic" fetch origin $($u.branch)
        git -C $Root -c "http.https://github.com/.extraheader=AUTHORIZATION: basic $basic" pull --ff-only origin $($u.branch)
    } else {
        git -C $Root fetch origin $($u.branch)
        git -C $Root pull --ff-only origin $($u.branch)
    }

    if ($LASTEXITCODE -ne 0) { throw "拉取失败（检查仓库是否存在、令牌是否有 Contents:Read 权限）" }

    $u.synced_at = (Get-Date).ToString("yyyy-MM-ddTHH:mm:ssK")
    $u.status = "synced"
    ($u | ConvertTo-Json -Depth 5) | Set-Content $UpstreamFile -Encoding UTF8
    Write-Host "已同步到 $($u.synced_at)"
}

function Invoke-Install {
    $src = Join-Path $Root ".opencode\agent"
    if (-not (Test-Path $src)) { throw "找不到 $src" }
    $dst = Join-Path $env:USERPROFILE ".config\opencode\agent"
    New-Item -ItemType Directory -Force -Path $dst | Out-Null
    Get-ChildItem $src -Filter *.md | ForEach-Object {
        Copy-Item $_.FullName (Join-Path $dst $_.Name) -Force
        Write-Host "已安装 $($_.Name) -> $dst"
    }
    Write-Host "重启 OpenCode 后在 agent 列表可见。"
}

if ($Pull)    { Invoke-Pull }
if ($Install) { Invoke-Install }
if ($Status -or (-not $Pull -and -not $Install)) { Show-Status }
