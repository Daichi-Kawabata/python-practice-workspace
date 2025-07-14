# Docker学習用スクリプト - Windows PowerShell版

Write-Host "==========================================" -ForegroundColor Green
Write-Host "Docker基本例の実行スクリプト" -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Green

# 1. シンプルなPythonアプリ
Write-Host "1. シンプルなPythonアプリをビルド・実行中..." -ForegroundColor Yellow
Set-Location examples/01_simple_python
docker build -t simple-python-app .
Write-Host "イメージサイズ確認:" -ForegroundColor Cyan
docker images simple-python-app
Write-Host "実行:" -ForegroundColor Cyan
docker run --rm simple-python-app
Set-Location ../..

Write-Host ""
Write-Host "2. 依存関係を含むアプリをビルド・実行中..." -ForegroundColor Yellow
Set-Location examples/02_requirements
docker build -t requirements-python-app .
Write-Host "イメージサイズ確認:" -ForegroundColor Cyan
docker images requirements-python-app
Write-Host "実行:" -ForegroundColor Cyan
docker run --rm -e DEBUG=true requirements-python-app
Set-Location ../..

Write-Host ""
Write-Host "3. FastAPIアプリをビルド中..." -ForegroundColor Yellow
Set-Location fastapi_example
docker build -t fastapi-docker-app .
Write-Host "イメージサイズ確認:" -ForegroundColor Cyan
docker images fastapi-docker-app
Write-Host "FastAPIアプリを起動（バックグラウンド）:" -ForegroundColor Cyan
docker run -d --name fastapi-container -p 8000:8000 fastapi-docker-app

Write-Host "5秒待機してからヘルスチェック..." -ForegroundColor Cyan
Start-Sleep -Seconds 5

# PowerShellでのHTTPリクエスト
try {
    $response = Invoke-RestMethod -Uri "http://localhost:8000/health" -Method Get
    Write-Host "ヘルスチェック結果:" -ForegroundColor Green
    $response | ConvertTo-Json -Depth 3
} catch {
    Write-Host "ヘルスチェックに失敗しました: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host "コンテナを停止・削除:" -ForegroundColor Cyan
docker stop fastapi-container
docker rm fastapi-container
Set-Location ..

Write-Host ""
Write-Host "4. マルチステージビルドアプリをビルド中..." -ForegroundColor Yellow
Set-Location multi_stage
docker build -t multistage-app .
Write-Host "イメージサイズ確認:" -ForegroundColor Cyan
docker images multistage-app
Write-Host "実行:" -ForegroundColor Cyan
docker run --rm -p 8001:8000 -d --name multistage-container multistage-app

Start-Sleep -Seconds 5

try {
    $response = Invoke-RestMethod -Uri "http://localhost:8001/health" -Method Get
    Write-Host "マルチステージアプリ ヘルスチェック結果:" -ForegroundColor Green
    $response | ConvertTo-Json -Depth 3
} catch {
    Write-Host "ヘルスチェックに失敗しました: $($_.Exception.Message)" -ForegroundColor Red
}

docker stop multistage-container
Set-Location ..

Write-Host ""
Write-Host "==========================================" -ForegroundColor Green
Write-Host "全ての例の実行が完了しました！" -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Green
Write-Host "作成されたイメージ:" -ForegroundColor Cyan
docker images | Select-String -Pattern "(simple-python-app|requirements-python-app|fastapi-docker-app|multistage-app)"

Write-Host ""
Write-Host "クリーンアップするには以下を実行:" -ForegroundColor Yellow
Write-Host "docker image prune -f" -ForegroundColor White

Write-Host ""
Write-Host "各アプリケーションを個別にテストするには:" -ForegroundColor Yellow
Write-Host "# FastAPIアプリ（ポート8000）:" -ForegroundColor White
Write-Host "docker run -d -p 8000:8000 --name test-fastapi fastapi-docker-app" -ForegroundColor White
Write-Host "curl http://localhost:8000 または http://localhost:8000/docs" -ForegroundColor White
Write-Host ""
Write-Host "# マルチステージアプリ（ポート8001）:" -ForegroundColor White
Write-Host "docker run -d -p 8001:8000 --name test-multistage multistage-app" -ForegroundColor White
Write-Host "curl http://localhost:8001 または http://localhost:8001/docs" -ForegroundColor White
