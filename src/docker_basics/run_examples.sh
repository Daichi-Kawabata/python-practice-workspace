#!/bin/bash
# Docker学習用スクリプト - Windows PowerShell版はrun_examples.ps1を使用

echo "=========================================="
echo "Docker基本例の実行スクリプト"
echo "=========================================="

# 1. シンプルなPythonアプリ
echo "1. シンプルなPythonアプリをビルド・実行中..."
cd examples/01_simple_python
docker build -t simple-python-app .
echo "イメージサイズ確認:"
docker images simple-python-app
echo "実行:"
docker run --rm simple-python-app
cd ../..

echo ""
echo "2. 依存関係を含むアプリをビルド・実行中..."
cd examples/02_requirements
docker build -t requirements-python-app .
echo "イメージサイズ確認:"
docker images requirements-python-app
echo "実行:"
docker run --rm -e DEBUG=true requirements-python-app
cd ../..

echo ""
echo "3. FastAPIアプリをビルド中..."
cd fastapi_example
docker build -t fastapi-docker-app .
echo "イメージサイズ確認:"
docker images fastapi-docker-app
echo "FastAPIアプリを起動（バックグラウンド）:"
docker run -d --name fastapi-container -p 8000:8000 fastapi-docker-app
echo "ヘルスチェック:"
sleep 5
curl -s http://localhost:8000/health | jq .
echo "コンテナを停止・削除:"
docker stop fastapi-container
docker rm fastapi-container
cd ..

echo ""
echo "4. マルチステージビルドアプリをビルド中..."
cd multi_stage
docker build -t multistage-app .
echo "イメージサイズ確認:"
docker images multistage-app
echo "実行:"
docker run --rm -p 8001:8000 -d --name multistage-container multistage-app
sleep 5
curl -s http://localhost:8001/health | jq .
docker stop multistage-container
cd ..

echo ""
echo "=========================================="
echo "全ての例の実行が完了しました！"
echo "=========================================="
echo "作成されたイメージ:"
docker images | grep -E "(simple-python-app|requirements-python-app|fastapi-docker-app|multistage-app)"

echo ""
echo "クリーンアップするには以下を実行:"
echo "docker image prune -f"
