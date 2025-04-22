#!/bin/bash

# Exit on error
set -e

# Configuration
APP_NAME="rpa-ms"
DOCKER_REGISTRY="your-registry.com"  # 替换为实际的 Docker 仓库地址
VERSION=$(date +%Y%m%d_%H%M%S)

echo "🚀 Starting deployment process for $APP_NAME..."

# Build Docker image
echo "📦 Building Docker image..."
docker build -t $APP_NAME:$VERSION -f deploy/Dockerfile .

# Tag the image
echo "🏷️ Tagging image..."
docker tag $APP_NAME:$VERSION $DOCKER_REGISTRY/$APP_NAME:$VERSION
docker tag $APP_NAME:$VERSION $DOCKER_REGISTRY/$APP_NAME:latest

# Push to registry
echo "⬆️ Pushing to registry..."
docker push $DOCKER_REGISTRY/$APP_NAME:$VERSION
docker push $DOCKER_REGISTRY/$APP_NAME:latest
