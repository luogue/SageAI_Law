# 最终待验收清单

当前权威状态：`artifacts/release_unblock/release-gates.json`。
旧轮次的构建退出码、OOM 日志和原始检测结果作为历史证据保留，不代表产品代码失败。

## 状态

| 项目 | 状态 |
| --- | --- |
| INDEPENDENT_DOCKER_ENV | UNAVAILABLE |
| BACKEND_DOCKER_BUILD | PASS |
| FRONTEND_DOCKER_BUILD | NOT_VERIFIED_ENV_BLOCKED |
| BACKEND_IMAGE_DB_SCAN | PASS |
| FRONTEND_IMAGE_DB_SCAN | NOT_VERIFIED |
| DOCKER_BUSINESS_REGRESSION | NOT_VERIFIED_ENV_BLOCKED |
| PRODUCTION_DB_STATUS | HEALTHY |
| PRODUCTION_FRONTEND_HEALTH | CONFIG_ERROR_FIXED_IN_CODE_NOT_DEPLOYED |
| PRODUCTION_FRONTEND_RUNNING_HEALTH | CONFIG_ERROR |
| CODE_RELEASE_GATE | BLOCKED |
| DATABASE_SWITCH_GATE | BLOCKED |
| PRODUCTION_DEPLOY_GATE | BLOCKED |

环境阻塞原因统一为：**当前没有资源满足要求的 Docker 验收环境，无法完成最终验证；不是已确认的代码失败。**

- CODE_RELEASE_GATE blocker：`DOCKER_ACCEPTANCE_ENV_UNAVAILABLE`。前端新镜像尚未生成，双镜像完整扫描及完整 Docker E2E 尚未完成。后端 PASS 沿用已有实际镜像构建和全部 11 层扫描证据，不宣称本轮进行了新构建。
- DATABASE_SWITCH_GATE：本地损坏库 4 条任务仍不完整，历史数据处置尚未批准；独立于生产健康库和代码发布。
- PRODUCTION_DEPLOY_GATE：代码门禁未 READY，healthcheck 修复尚未完成最终 Docker 验证和部署。未部署是当前事实，不得通过本清单自动部署。
- 生产数据库 HEALTHY 沿用 2026-09-09 15:17:23（北京时间）的只读复核：完整性检查通过、11 条任务可读、缺失报告引用 0。本轮状态整理没有重新连接生产。

## Healthcheck 最小修复

生产探针访问 `localhost`，解析到 `::1`，而 Nginx 仅监听 IPv4，导致 connection refused；显式 IPv4 页面与代理 `/health` 返回 200。真实服务正常，Docker unhealthy 是配置错误。

`Dockerfile.frontend` 和 `docker-compose.yml` 已明确使用 `http://127.0.0.1:80/`，匹配仓库 `nginx.conf` 的 `listen 80`、`location /` 和 `index.html`。保留 wget HTTP 探测和非零失败退出。本轮补充原因注释及静态回归，没有修改生产实例。

本轮执行：

```text
node --test scripts/frontend-healthcheck.test.mjs
exit code: 0
tests: 5; pass: 5; fail: 0
```

覆盖 Dockerfile/Compose 地址一致性、真实 HTTP 探针和失败传播、Nginx 端口和页面资源匹配，并验证能拒绝 localhost、IPv6、错误端口/路径及永远成功的探针。这是静态回归，不替代最终 Docker E2E。

## 仅在获得可用验收环境后执行

触发条件仅为：资源充足的独立 Docker 主机、可用 CI runner、现成 Docker context，或本机后续具备可用 Docker/WSL2/虚拟化环境。禁止在原资源不足的生产主机上重试。

以下命令是未来执行清单，本轮未执行。先确认选中的 Docker context 指向独立验收环境。记录宿主机 CPU、总/可用内存、swap、磁盘和 cgroup 限制；不能只看总内存。使用充足资源，不设置已导致 OOM 的低内存上限，不删减正常构建步骤。

```sh
docker context show
docker version
docker info
docker buildx version
docker buildx inspect --bootstrap
git rev-parse HEAD
git status --short
node --test scripts/frontend-healthcheck.test.mjs
```

固定待发布源码快照，同时记录未提交修改/文件哈希（仅 commit 不足以标识当前工作区）。在独立主机的新证据目录内记录每条命令的真实退出码；日志通过管道保存时须保留构建命令自身的退出码。

```sh
docker buildx build --load --no-cache --progress=plain -f Dockerfile.backend -t sageai-acceptance:backend --iidfile backend.iid .
docker buildx build --load --no-cache --progress=plain -f Dockerfile.frontend -t sageai-acceptance:frontend --iidfile frontend.iid .
docker image inspect sageai-acceptance:backend sageai-acceptance:frontend
docker image save -o acceptance-images.tar sageai-acceptance:backend sageai-acceptance:frontend
```

随后仅做以下最终验收：

1. 对两镜像分别创建不启动的临时容器并 `docker export` 检查最终文件系统；检查 `docker image save` 中每一层。扫描 SQLite 文件名/文件头、WAL/SHM/journal、压缩备份、恢复候选、业务数据目录；不要把普通含 db 的代码误判为数据。记录镜像 ID、层数及命中列表，不能只检查最终合并文件系统。
2. 用独立网络和新命名持久卷启动最终双镜像。验收配置使用全新 SQLite 数据库、独立测试凭据、隔离端口与容器名称；不得直接使用带固定生产容器名和卷名的仓库 Compose 启动。检查迁移、双容器 healthcheck 与 HTTP 状态，记录容器实际限制和 OOM/重启次数。
3. 从真实前端页面经 Nginx 代理登录，创建任务和报告，读取历史任务/报告，验证中文下载；保存请求、响应、UI 和持久化证据。
4. 在测试数据库内触发异常事务并证明 rollback；重启两个测试容器后确认任务、报告和历史详情仍存在，数据库检查通过。
5. 经真实前端依次审查租赁、承揽、运输、投资、股东、劳动合同；比较 UI 画像、发送参数、后端生效参数。验证非租赁无“个人租客/租客/居住用途”污染、类型切换刷新身份和场景、手动通用偏好保留。真实容器结果不得用 pytest 或模拟页面代替；记录实际审查模式。
6. 汇总两次构建、两次完整镜像扫描、完整 Docker E2E 的证据后才重算 CODE_RELEASE_GATE。若进入未来生产发布决策，另行只读复核生产可达性、数据库健康和前端实际服务状态；本清单不授权部署、数据库切换或历史数据处置。

最终验收通过也不改变本地 DATABASE_SWITCH_GATE；仍等待单独的数据处置批准。
