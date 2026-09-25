# 发布解阻验证：第二轮最终证据

时间：2026-09-09，北京时间 14:56–15:10。没有修改应用代码，没有部署、切换数据库、删除历史数据或写入原库。

| 项目 | 最终结论 |
|---|---|
| SSH | 已恢复；sshd active，22 端口监听，主机在线。 |
| OOM | **确认本轮隔离测试容器发生两次内核 cgroup OOM**；不将其归因到更早的 SSH 故障。 |
| FRONTEND_DOCKER_BUILD | **FAIL** |
| BACKEND_IMAGE_DB_SCAN | **PASS** |
| FRONTEND_IMAGE_DB_SCAN | **FAIL**：最终镜像不存在，未完成扫描验收。 |
| DOCKER_BUSINESS_REGRESSION | **FAIL**：后端功能断言通过，但存在 worker OOM；前端及前后端联合链路缺失。 |
| PRODUCTION_DB_STATUS | **HEALTHY**：本轮重新采集和校验；不是引用此前 11:48 结果。 |
| CODE_RELEASE_GATE | **BLOCKED** |
| DATABASE_SWITCH_GATE | **BLOCKED**：本轮没有新增数据处置授权。 |
| PRODUCTION_DEPLOY_GATE | **BLOCKED** |

## SSH、资源与 OOM 的证据边界

14:56 确认 sshd 从 9 月 5 日起持续运行，主 PID 1883377；IPv4/IPv6 22 端口均监听。内存总量 1608 MB，可用约 672 MB；swap 2047 MB，已用 0；磁盘可用 24 GB；没有上一轮遗留 build/node/npm/vite 负载。

上一轮 11:45–13:00 的 kernel/system 日志没有找到 OOM kill、sshd 被杀的证据。首轮 Node/V8 heap out of memory 有构建日志，但它不等于内核 OOM kill，更不能证明此前 SSH 超时由 OOM 导致。

本轮受限构建出现明确资源压力：主机 `vm.swappiness=0`；容器 512 MiB 上限下实际使用约 506 MiB；`memory.events max=105315, oom=0, oom_kill=0`；swap 没有使用；I/O 等待约 74%–80%，累计重复读盘约 16.3 GB。没有改生产内核参数。核对容器 `b7d12367a40c…` 的来源和 `npm run build` 命令后，仅停止该验证容器。最终退出 137 是此次停止产生的结果，不能仅凭它认定 OOM。

**随后后端验证阶段出现独立的新事件**：

- 15:07:23：`CONSTRAINT_MEMCG`，`Killed process 2421767 (gunicorn)`。
- 15:07:37：`CONSTRAINT_MEMCG`，`Killed process 2421768 (gunicorn)`。
- 两条日志均指向 cgroup/container `3fb943e9335a0de1bb9b909fb23b88276e41c664886a3db9b246b20b554695f4`，已通过 docker inspect 确认名称为 `/sageai-release-verify-20260909-round2-backend`，使用独立新卷，内存上限 384 MiB。

该测试容器中的 Gunicorn master 存活并补充 worker，所以功能断言仍能通过；不能用容器 `OOMKilled=false` 或 HTTP 200 否认 worker 被杀的内核证据。已据此将最终业务验收判为 FAIL。没有把此事件描述为生产容器或 sshd 被杀。

15:09 最终检查：测试容器已停止，无遗留构建进程；sshd active，CPU 约 98% idle，可用内存约 646 MB，磁盘可用 24 GB；生产三个容器 ID 与启动时间保持原状。

证据：[前次时段日志](round2-resource-evidence.json)、[本轮构建资源](round2-build-resources.json)、[停止已确认负载](round2-stop-owned-build.json)、[最终内核日志](round2-host-final.json)、[OOM 容器归属](round2-test-container-oom-attribution.json)。

## 前端实际构建

优先取回了先前重试的真实结果：后端 exit=0，前端达到 1800 秒超时，exit=124。前端停在 Vite transforming 阶段，没有成功镜像。

本轮执行了一次新的生产构建。原 Dockerfile、依赖锁定、`npm run build`、生产模式和 minification 都没有改变。仅在隔离构建 context 内增加 npm 的 Node 堆资源参数 `--max-old-space-size=768`，物理内存限 512 MiB、总内存加 swap 限 1536 MiB；没有关闭任何构建检查。npm 参数传递机制见 [npm 官方配置文档](https://docs.npmjs.com/cli/v8/using-npm/config/#node-options)。

实测持续内存回收/读盘停滞后，为保护同机业务，停止了已确认的验证容器；最终 exit=137，判 FAIL，属于已观察到的资源限制，未发现需要修改应用代码的编译错误。没有继续无意义重复构建。

`docker image inspect sageai-release-verify-20260909:frontend` 实际 exit=1，`No such image`。没有选用旧线上镜像冒充最终镜像。

证据：[取回的原任务退出码](round2-retrieved-build-result.json)、[本轮构建命令/退出码](round2-build-result.json)、[本轮构建日志](round2-build-frontend.log)、[镜像不存在](round2-frontend-image.json)。

## 最终后端镜像扫描

镜像 ID：`sha256:b52381b00707382f98cc624f8d7295b7abd5a67e5ea7dab4d82252556b7a5774`。

实际 `docker export` 扫描最终文件系统 **13540 个文件**，并 `docker image save` 扫描 **全部 11 层**。依据为数据库/备份文件后缀、SQLite 文件头签名，以及业务数据/恢复证据目录中的实际文件。

发现数 0：没有 app.db、sqlite/sqlite3、WAL/SHM/journal、archive.sqlite.gz、数据库备份、本地业务目录载荷或恢复副本。允许空的 `/app/data` 持久卷目录；没有按名字包含 `db` 一概禁止普通代码文件。

证据：[完整逐层扫描结果](round2-backend-scan.json)。前端扫描因最终镜像不存在判 FAIL，不能仅凭 ignore 配置判 PASS。

## 真实 Docker 后端子项与整体失败

使用全新卷 `sageai-release-verify-20260909-round2-db`、独立内部网络、两个 Gunicorn worker；没有挂生产卷或损坏原库。未用 pytest 替代容器检查。

已通过功能断言：初始化及 6 个 migration、后端启动及 HTTP 健康检查、真实密码登录、创建任务、状态持久化、保存/读取报告、任务/报告历史查询、两次容器重启、异常事务 rollback、中文文件名 md/docx/pdf 下载响应头。

六类审查调用实际容器 HTTP `/review-v2/checklist`，明确使用规则模式 `use_llm=false`：租赁、承揽、运输、投资、股东、劳动。检查类型对应身份、非租赁画像不含租客/居住用途、手动风险偏好与交易地位保留；实际每条规则的 `decision_trace.bargaining_power` 与返回画像一致，样本已存入证据。云端模型调用和前端 UI 不在这些已通过断言范围内。

任务/报告写入在容器内调用真实存储函数，登录、审查、查询和导出走真实 HTTP。该结果只能证明后端子项，不能冒充前端到后端完整上传链路通过。加上已确认的 worker OOM，最终稳定性与整体业务验收均 FAIL。

证据：[原始断言结果](round2-backend-runtime.json)、[结合内核证据后的最终裁定](round2-runtime-verdict.json)。

## 当前生产只读复核

本轮 15:00 重新通过 SFTP 获取主文件/WAL/SHM，两次采集内容和元数据稳定，在新建隔离副本上执行 SQLite 检查。15:09 又核对生产三个文件的 SHA256，仍与本轮已校验副本一致。

- SQLite；实际 `DATABASE_URL=sqlite:////app/data/app.db`。
- 卷 `sageai-db-data`；宿主路径 `/var/lib/docker/volumes/sageai-db-data/_data/app.db`。
- integrity_check=ok，quick_check=ok，foreign_key_check 无错误。
- 13 表可读；task_record 11 条全部可读；缺失 report 引用 0。
- 当前线上版本 5.0.0，后端 image ID `sha256:a1954471f1473036a7dda7a1250b169a8be6b4b3bf0415ce8956a7e362523332`；部署目录没有可解析的 git commit，commit=UNKNOWN。
- 后端 /health HTTP 200；前端 IPv4 HTTP 200，但其既存 Docker healthcheck 仍因访问 IPv6 localhost 报 unhealthy。本轮只读检查，没有更改线上健康配置。
- 磁盘可用 24 GB，sshd 可达。生产 DB 状态为 HEALTHY；这不抹除前端健康检查的既存异常。

证据：[当前生产完整复核](round2-production.json)、[最终主机及数据库字节复核](round2-host-final.json)。

## 剩余最小阻塞项

提供内存足够的独立 Docker 验证主机，完成成功的前端生产构建、最终前端镜像扫描，以及包含前端、且无 worker OOM 的完整 Docker 业务回归。已向用户请求该资源；不能靠修改生产内核设置或接受数据缺口替代技术验收。

生产发布还需满足代码门禁并复核当前服务健康，包括既存的前端 healthcheck 异常。数据库切换继续等待用户另行批准历史数据处置，本轮不处理。

本地原库及 WAL、SHM 的大小和 SHA256 与上一轮证据一致；SHM 的 mtime 较上一轮发生变化，来源未确证，不能声称全部元数据未变。本轮没有向这些文件执行写操作，也没有据此扩大数据库调查。证据：[原文件对照](round2-source-preservation.json)。

机器可读最终状态：[三个门禁](round2-release-gates.json)。
