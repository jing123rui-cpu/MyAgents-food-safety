<#
.SYNOPSIS
    同步 MyAgents agent 仓库：拉取更新 / 提交并推送 / 安装到 OpenCode 全局目录。

.EXAMPLE
    .\sync.ps1 -Pull
    从 origin 拉取更新（--ff-only，本地有改动时失败，不覆盖）。

.EXAMPLE
    .\sync.ps1 -Push
    自动提交所有改动并推送，提交信息为 "chore: sync yyyy-MM-dd HH:mm"。

.EXAMPLE
    .\sync.ps1 -Push -Message "feat: 新增检查点"
    指定提交信息后推送。

.EXAMPLE
    .\sync.ps1 -Pull -Push
    先拉取，再提交并推送。

.EXAMPLE
    .\sync.ps1 -Install
    把 .opencode/agent 下的 agent 复制到 ~/.config/opencode/agent，全局可用。

.EXAMPLE
    .\sync.ps1 -Status
    查看仓库状态与远端信息。
#>
param(
    [switch]$Pull,
    [switch]$Push,
    [string]$Message = "",
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

function Save-Upstream([string]$status) {
    $u = Get-Upstream
    $u.synced_at = (Get-Date).ToString("yyyy-MM-ddTHH:mm:ssK")
    $u.status = $status
    ($u | ConvertTo-Json -Depth 5) | Set-Content $UpstreamFile -Encoding UTF8
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
        Write-Host "工作区尚未初始化 git 仓库。"
    }
}

function Invoke-Pull {
    $u = Get-Upstream
    if (-not (Test-Path (Join-Path $Root ".git"))) {
        throw "工作区尚未初始化 git 仓库，请先执行: git init -b $($u.branch)"
    }

    $remotes = git -C $Root remote
    if (-not $remotes) {
        Write-Host "未配置 remote，正在添加 origin -> $($u.repo)"
        git -C $Root remote add origin $u.repo
    }

    # 仅当显式传入 Token 时才用临时 header；SSH 远端不需要
    if ($Token) {
        $basic = [Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes("x-access-token:$Token"))
        git -C $Root -c "http.https://github.com/.extraheader=AUTHORIZATION: basic $basic" fetch origin $($u.branch)
        git -C $Root -c "http.https://github.com/.extraheader=AUTHORIZATION: basic $basic" pull --ff-only origin $($u.branch)
    } else {
        git -C $Root fetch origin $($u.branch)
        git -C $Root pull --ff-only origin $($u.branch)
    }

    if ($LASTEXITCODE -ne 0) { throw "拉取失败：检查远端是否存在、网络是否可用、是否有推送/读取权限。" }

    Save-Upstream "synced"
    Write-Host "已同步: $((Get-Date).ToString('yyyy-MM-dd HH:mm:ss'))"
}

function Invoke-Push {
    $u = Get-Upstream
    if (-not (Test-Path (Join-Path $Root ".git"))) {
        throw "工作区尚未初始化 git 仓库。"
    }

    $changes = git -C $Root status --porcelain
    if ($changes) {
        if (-not $Message) {
            $Message = "chore: sync $(Get-Date -Format 'yyyy-MM-dd HH:mm')"
        }
        Write-Host "待提交改动:"
        $changes | ForEach-Object { Write-Host "  $_" }
        # 同步时间在提交前写入，避免推送后又留下未提交改动
        Save-Upstream "synced"
        git -C $Root add -A
        git -C $Root commit -m $Message
        if ($LASTEXITCODE -ne 0) { throw "提交失败。" }
    } else {
        Write-Host "没有待提交的改动。"
    }

    if ($Token) {
        $basic = [Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes("x-access-token:$Token"))
        git -C $Root -c "http.https://github.com/.extraheader=AUTHORIZATION: basic $basic" push origin $($u.branch)
    } else {
        git -C $Root push origin $($u.branch)
    }

    if ($LASTEXITCODE -ne 0) { throw "推送失败：检查远端地址与认证方式。" }

    Write-Host "已推送: $((Get-Date).ToString('yyyy-MM-dd HH:mm:ss'))"
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
    Write-Host "重新打开 OpenCode 即可在 agent 列表看到。"
}

if ($Pull)    { Invoke-Pull }
if ($Push)    { Invoke-Push }
if ($Install) { Invoke-Install }
if ($Status -or (-not $Pull -and -not $Push -and -not $Install)) { Show-Status }

