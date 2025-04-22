# RPA-MS 部署指南

本文档详细说明了如何部署 RPA-MS 服务到 Kubernetes 集群。

## 目录

- [前置要求](#前置要求)
- [部署文件说明](#部署文件说明)
- [配置修改](#配置修改)
- [部署步骤](#部署步骤)
- [验证部署](#验证部署)
- [故障排除](#故障排除)

## 前置要求

在开始部署之前，请确保您的环境满足以下要求：

1. **Docker**
   - 已安装 Docker（推荐 20.10.x 或更高版本）
   - Docker 守护进程正在运行
   - 有权限执行 Docker 命令

2. **Kubernetes**
   - 已配置好 Kubernetes 集群
   - 已安装 kubectl 命令行工具
   - kubectl 已正确配置集群访问凭证

3. **Docker Registry**
   - 可访问的 Docker 镜像仓库
   - 已配置 Docker 仓库的访问凭证

4. **其他要求**
   - bash shell 环境
   - 具有项目目录的写入权限

## 部署文件说明

部署相关的文件都位于 `deploy` 目录下：

1. **Dockerfile**
   - 用于构建应用容器镜像
   - 基于 Python 3.11 slim 镜像
   - 包含应用运行所需的所有依赖

2. **deploy.sh**
   - 自动化部署脚本
   - 处理镜像构建、标记和推送
   - 更新 Kubernetes 部署

3. **kubernetes.yaml**
   - Kubernetes 资源定义文件
   - 包含 Deployment 和 Service 配置
   - 设置了资源限制和健康检查

## 配置修改

在部署之前，需要修改以下配置：

1. **deploy/deploy.sh**
   ```bash
   # 修改 Docker 仓库地址
   DOCKER_REGISTRY="your-registry.com"  # 替换为实际的 Docker 仓库地址
   ```

2. **deploy/kubernetes.yaml**
   ```yaml
   # 修改镜像地址
   image: your-registry.com/rpa-ms:latest  # 替换为实际的镜像地址
   
   # 根据需要调整资源限制
   resources:
     requests:
       cpu: "100m"      # 根据实际需求调整
       memory: "128Mi"  # 根据实际需求调整
     limits:
       cpu: "500m"      # 根据实际需求调整
       memory: "512Mi"  # 根据实际需求调整
   ```

## 部署步骤

1. **登录 Docker 仓库**
   ```bash
   docker login your-registry.com
   ```

2. **赋予部署脚本执行权限**
   ```bash
   chmod +x deploy/deploy.sh
   ```

3. **首次部署到 Kubernetes**
   ```bash
   # 创建 Kubernetes 资源
   kubectl apply -f deploy/kubernetes.yaml
   ```

4. **执行部署脚本**
   ```bash
   ./deploy/deploy.sh
   ```

## 验证部署

1. **检查 Pod 状态**
   ```bash
   kubectl get pods -l app=rpa-ms
   ```
   所有 Pod 应该显示为 `Running` 状态

2. **检查服务状态**
   ```bash
   kubectl get svc rpa-ms
   ```
   查看服务的外部 IP 地址

3. **验证应用健康状态**
   ```bash
   curl http://<service-ip>/health
   ```
   应返回成功状态

## 故障排除

1. **镜像构建失败**
   - 检查 Dockerfile 中的依赖是否正确
   - 确保 requirements.txt 文件存在且内容正确
   - 查看构建日志：`docker logs <container-id>`

2. **Pod 启动失败**
   - 查看 Pod 详细信息：`kubectl describe pod <pod-name>`
   - 查看 Pod 日志：`kubectl logs <pod-name>`
   - 检查资源限制是否合理

3. **服务无法访问**
   - 确认 Service 配置正确：`kubectl describe svc rpa-ms`
   - 检查防火墙规则
   - 验证健康检查端点是否正常响应

4. **常见错误处理**
   - ImagePullBackOff：检查镜像仓库访问权限
   - CrashLoopBackOff：检查应用启动配置
   - Pending：检查集群资源是否充足

## 注意事项

1. 确保在生产环境部署前已经完成了充分的测试
2. 定期检查和更新依赖包的版本
3. 监控应用的资源使用情况，适时调整资源限制
4. 保持 Docker 镜像的安全更新
5. 定期备份关键数据

