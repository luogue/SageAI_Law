# SageAI 上线前检查清单

> 在正式部署到生产环境之前，请逐项确认以下检查项。

---

## 一、安全配置

- [ ] 所有敏感配置已通过环境变量注入，无硬编码
  - `ARK_API_KEY`、`ARK_ENDPOINT_ID`
  - `ZHIPU_API_KEY`、`DASHSCOPE_API_KEY`、`DEEPSEEK_API_KEY`
  - `JWT_SECRET_KEY`（长度 >= 64 字符随机字符串）
  - `ADMIN_TOKEN`、`API_SECRET_KEY`
- [ ] `CORS_ORIGINS` 已配置为实际域名（不允许 `*`）
- [ ] HTTPS 已启用（通过 Nginx 反向代理或直接配置）
- [ ] 安全头部已配置：`X-Content-Type-Options`、`X-Frame-Options`、`CSP`
- [ ] 密码哈希使用 bcrypt（强度因子 >= 12）
- [ ] 生产环境 `.env.production` 中 `LLM_MOCK_MODE=false`
- [ ] 生产环境 `.env.production` 中 `DEBUG_PROMPT=false`
- [ ] API Key 不出现在日志或错误返回中
- [ ] `ENABLE_SENSITIVE_FILTER=true`、`ENABLE_RATE_LIMIT=true`

## 二、数据库与持久化

- [ ] 数据库文件路径可写（Docker 中使用 named volume）
- [ ] 数据库已执行初始化（表已创建）
- [ ] SQLite PRAGMA 优化已配置（WAL 模式）
- [ ] 备份脚本 `backup.sh` 已配置 crontab 定时执行
- [ ] 最近一次备份已验证可恢复

## 三、日志与监控

- [ ] 日志目录 `/app/logs` 可写
- [ ] 日志已配置按天滚动，保留 30 天
- [ ] 日志格式包含：时间、请求ID、用户ID、IP、耗时、状态码
- [ ] 健康检查 `GET /health` 返回 `{"status": "ok"}`
- [ ] 健康检查 `GET /ping` 返回 `{"status": "ok"}`
- [ ] （可选）监控告警已配置（CPU、内存、请求量）

## 四、前端

- [ ] 静态文件已构建（`npm run build`）
- [ ] Gzip 压缩已启用
- [ ] 第三方库已代码分割（vue-vendor、element-plus、echarts 等）
- [ ] 生产环境 disable console / debugger
- [ ] `.env.production` 中 `VITE_API_BASE_URL` 已配置正确
- [ ] `vite.config.js` 生产模式 sourcemap 已关闭

## 五、Nginx / 反向代理

- [ ] 静态文件正确托管（`/` 指向 `dist/`）
- [ ] API 反向代理 `/api/` → `http://backend:8000`
- [ ] 静态文件强缓存（JS/CSS 1 年，HTML 不缓存）
- [ ] API 路由不缓存
- [ ] Gzip 压缩已启用
- [ ] 安全头部已配置
- [ ] client_max_body_size 已设置（50M）

## 六、Docker 部署

- [ ] `docker-compose.yml` 配置已检查
- [ ] 数据库 volume `sageai-db-data` 已创建
- [ ] 健康检查 `HEALTHCHECK` 已配置
- [ ] 非 root 用户运行容器
- [ ] `.env.production` 文件已准备

## 七、网络与防火墙

- [ ] 防火墙已开放必要端口：80（HTTP）、443（HTTPS）
- [ ] 后端端口 8000 仅内网访问（不直接公网暴露）
- [ ] SSL 证书已配置并生效

## 八、性能

- [ ] Gunicorn worker 数量合理（`2 * CPU 核数 + 1`）
- [ ] 请求超时 300 秒已配置
- [ ] Gzip 压缩已启用（>500 字节响应）
- [ ] （可选）已完成压力测试
- [ ] （可选）CDN 已配置（静态文件加速）

## 九、部署流程验证

- [ ] `deploy.sh` 已测试可正常运行
- [ ] `rollback.sh` 已测试可正常回滚
- [ ] `backup.sh` 已测试可正常备份和恢复
- [ ] 镜像构建成功（`docker compose build`）

## 十、功能验证（部署后）

- [ ] 首页能正常访问
- [ ] 用户注册/登录正常
- [ ] 合同上传和审查正常
- [ ] 合同审查报告正常生成
- [ ] 批量审查正常
- [ ] 反馈功能正常
- [ ] 管理后台正常
- [ ] API 文档 `/docs` 正常（可选关闭）

---

## 部署完成后建议

1. **关闭 Swagger 文档**（生产环境）：
   ```python
   app = FastAPI(title="...", docs_url=None, redoc_url=None)
   ```

2. **配置域名和 SSL**：使用 Let's Encrypt 免费证书（certbot）

3. **配置监控**：推荐 Prometheus + Grafana 或简单的 UptimeRobot

4. **定期检查日志**：`docker compose logs -f backend | grep ERROR`
