@echo off
chcp 65001 >nul
cd /d "%~dp0"

echo ========================================
echo 配置 Git 仓库并推送到 GitHub
echo ========================================
echo.

REM 设置 Git 用户信息
echo [1/5] 配置 Git 用户信息...
git config user.name "jadevase"
git config user.email "jadevase@users.noreply.github.com"
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Git 配置失败，请确认已安装 Git
    pause
    exit /b 1
)
echo ✅ Git 用户信息配置成功
echo.

REM 添加所有文件
echo [2/5] 添加所有文件到暂存区...
git add .
if %ERRORLEVEL% NEQ 0 (
    echo ❌ 添加文件失败
    pause
    exit /b 1
)
echo ✅ 文件添加完成
echo.

REM 提交更改
echo [3/5] 提交初始版本...
git commit -m "Initial commit: 心理学知识库 GitHub 部署

- 添加完整的知识库结构（每日学习内容 + 练习题）
- 配置 GitHub Actions 自动同步工作流
- 配置 GitHub Pages 在线浏览页面
- 添加详细的部署和使用指南

作者：jadevase
日期：2026-04-09"
if %ERRORLEVEL% NEQ 0 (
    echo ⚠️  提交失败（可能是空仓库或没有更改）
)
echo.

REM 添加远程仓库
echo [4/5] 添加 GitHub 远程仓库...
echo 远程仓库地址：https://github.com/jadevase/psychology-knowledge-base.git
git remote remove origin 2>nul
git remote add origin https://github.com/jadevase/psychology-knowledge-base.git
if %ERRORLEVEL% NEQ 0 (
    echo ⚠️  添加远程仓库失败
)
echo ✅ 远程仓库配置完成
echo.

REM 推送分支
echo [5/5] 推送到 GitHub...
echo.
echo ⚠️  注意：首次推送需要输入 GitHub 用户名和密码（或个人访问令牌）
echo.
echo 如果是第一次推送，请输入你的 GitHub 凭据...
echo.
git branch -M main
git push -u origin main
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ❌ 推送失败
    echo.
    echo 可能的原因：
    echo 1. 未安装 Git
    echo 2. 网络连接问题
    echo 3. 需要配置 GitHub 个人访问令牌
    echo.
    echo 解决方案请参考 DEPLOYMENT_GUIDE.md
    pause
    exit /b 1
)
echo.
echo ========================================
echo ✅ 部署成功！
echo ========================================
echo.
echo 你的知识库已上传到：
echo https://github.com/jadevase/psychology-knowledge-base
echo.
echo 下一步操作：
echo 1. 启用 GitHub Actions: 访问仓库 → Actions → Enable workflows
echo 2. 配置 GitHub Pages: Settings → Pages → Source: main branch, Folder: /docs
echo 3. 访问在线页面：https://jadevase.github.io/psychology-knowledge-base/
echo.
pause
