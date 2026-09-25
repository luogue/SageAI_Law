# 发布解阻验证报告

日期：2026-09-09。此次仅处理发布验证及实测发现的三个阻塞问题。没有部署、切库、删除任务或覆盖原数据库。

## 1. 四条损坏任务能否进一步恢复

**可以补证字段，仍不能完整恢复：33/37 条完整任务，另外 4 条各有 9/17 个可证字段。**

| id | task_id | 日志确认的文件 | 完成日志时间（北京时间） | user_id / record_id / remaining_bonus | 完整结果 |
|---|---|---|---|---|---|
| 34 | c6daf70a-ed9c-443a-9ad6-0b742f51ce76 | 同一房屋买卖合同签订三份“阴阳合同”，法院如何认定效力？.txt；3950 bytes | 2026-06-14 14:50:00 | 1 / 3 / 2 | 未找到 |
| 35 | 7ea566e9-1f67-4d2e-bceb-a88c405081be | 退休人员返聘协议（模板）.docx；20059 bytes | 2026-06-14 18:41:55 | 1 / 4 / 1 | 未找到 |
| 36 | 89ff9724-8eb3-43c5-8169-6071a0ba2bdc | 同上 | 2026-06-14 18:57:53 | 1 / 4 / 0 | 未找到 |
| 37 | e451edda-230a-49f9-8c23-7668892fb607 | 同上 | 2026-06-14 20:35:33 | 1 / 4 / 2 | 未找到 |

每条可证字段：`id, task_id, filename, file_size, user_id, status=completed, record_id, remaining_bonus, trace_id`。完成状态及业务字段来自当时日志，尚未写入任何候选任务行。

每条无法确认：`progress, result, error, metadata_json, validation_json, summary_json, created_at, updated_at`。日志事件时间不冒充数据库时间；完成日志不用于猜测 progress=100 或 error=NULL。

对应 trace_id 分别为 `trace_mqdfbn0s_wkkoo0rob`、`trace_mqdnlg1f_0xiudlonb`、`trace_mqdo63g5_zrnuncdop`、`trace_mqdrnnga_aiw5y7huf`。报告保存日志长度分别为 912、860、891、1796 字符，这不是已恢复的正文。

报告 3、4 曾真实保存；当前可读报告表中均不存在。35、36 的报告 4 分别有 18:56:39、20:32:38 的成功删除日志，随后编号被复用。未找到足够证据确认 34、37 对应报告最终消失的原因。

已检查包括忽略文件在内的工作区 UUID/trace 日志、其他数据库、历史快照、桌面/下载/文档中的匹配文件，以及 Chrome/Edge 所有已发现的本应用 IndexedDB。五个 LevelDB 共解析 2154 个底层记录；四个 ContractReviewDB 的对象存储均没有可提取合同记录。在已检查的本地范围内未发现其他匹配数据库或可用历史备份。生产主机上的旁路日志/历史备份搜索尚未穷尽，因后续 SSH 故障无法继续；不能宣称所有环境都已穷尽。此前官方恢复的旧页残片只是现存 report 2 的重复，不是新增报告。

桌面存在与 35–37 同名、同大小的 DOCX，但没有上传时哈希，不能证明当时输入字节完全相同。同目录 `_review.txt` 是更早的 9828 字符报告，内容/时间/长度无法与这三次任务对应，不计为恢复。

**四条都影响用户可见历史，均不能判定可安全丢弃。建议逐条人工处理，保留原始证据和独立残缺字段清单；不自动删除，也不插入伪造的完整 completed 行。**

证据：[逐条字段清单](../db_recovery/four-task-final-evidence.json)、[trace 日志](../db_recovery/damaged-task-trace-evidence.json)、[其他数据库](../db_recovery/other-db-evidence.json)、[文件证据](../db_recovery/sidecar-files-evidence.json)、[浏览器离线检查](../db_recovery/browser_evidence/inspection.json)。

## 2. 14 个缺失 report_id=1 引用的原因

**这是早于本次损坏的历史删除/引用维护问题，与 4 条任务的物理页损坏分开。**

任务 id 为 `2,3,5,6,7,8,9,10,11,12,13,17,22,26`。日志证实 report 1 曾可 GET，且 2026-06-11 至 06-14 有 14 次成功删除 `/api/records/1`；不是一个从未存在的报告。不同历史报告重复使用编号 1。

`backend/storage/crud.py::delete_record` 只删除 Record，没有处理 `TaskRecord.record_id`；该列没有外键。`Record.id` 是普通 SQLite INTEGER PRIMARY KEY，删除最大编号后可复用。因此不能把这 14 个引用统一接到新造的“报告 1”上。

独立候选副本上：14 个任务均出现在历史列表；14 个详情的 result 与候选原字段一致。报告路由 `/api/records/1`、`/api/download/1` 返回 404；前端若跳转报告编号页，仍不能查看已删除报告，不能把 API 任务详情可读等同于所有 UI 路径正常。

任务导出使用 task.result，不依赖报告表。但实测另外发现中文响应头编码 bug，修复后 14×3=42 次任务导出全部 HTTP 200，新报告三种导出也通过。该修复不恢复任何已删除报告。

无需因本地这 14 个引用对健康生产库执行迁移。若处理本地历史库，需要先决定是否保留带审计标记的引用、清理引用或生成明确标注来源的派生报告；不能自动恢复旧编号 1。删除后的引用维护/编号复用仍是后续明确的业务修复项，本阶段没有扩展修改其数据语义。

证据：[历史引用时间线](../db_recovery/report1-final-evidence.json)、[修复前实测](history-acceptance-before-fix.json)、[修复后实测](history-acceptance.json)。

## 3. Docker 实际构建

本机没有可用 Docker 引擎。实际构建在已恢复访问的主机上，以独立目录 `/var/tmp/sageai-release-verify-20260909`、独立镜像标签执行；没有构建或替换正在运行的生产容器标签，没有挂载生产业务卷。

后端首次及修复后构建均成功。修复后镜像短 ID 为 `b52381b00707`。前端首次构建失败，证据为 Node 在隔离的 512 MB 上限下发生 heap out of memory；不能把该失败描述为 Vue 编译错误。

前端以 1280 MB 内存上限重试后，SSH 握手持续超时，最终退出码和后续独立容器结果尚未取回，**前端 build / 完整 Docker 业务链路未判通过**。

实际命令为：

```sh
DOCKER_BUILDKIT=0 docker build --memory=512m --memory-swap=2g \
  --cpu-period=100000 --cpu-quota=50000 --cpu-shares=128 --force-rm \
  -f Dockerfile.backend -t sageai-release-verify-20260909:backend .
DOCKER_BUILDKIT=0 docker build --memory=1280m --memory-swap=2g \
  --cpu-period=100000 --cpu-quota=50000 --cpu-shares=128 --force-rm \
  -f Dockerfile.frontend -t sageai-release-verify-20260909:frontend .
```

后续脚本仅计划使用 `sageai-release-verify-20260909-fresh-db` 新卷和独立内部网络，验证 migration、双端健康检查、六类 V2/画像、任务/报告持久化和两次重启。**脚本已提交运行不等于测试已通过；结果未回收的项目均保持未验证。** 云端模型调用也未在本阶段完成验证，既有规则模式结果不能冒充云端端到端通过。

原始记录：[首轮构建退出码](initial-build-result.json)、[前端 OOM 日志](initial-build-frontend.log)、[重建派发](docker-rebuild-dispatch.json)。

## 4. 镜像是否彻底排除了数据库文件

**目前不能最终证明。** 实际首轮后端镜像内未发现 app.db、WAL、SHM，但发现测试哨兵 `/app/release_exclusion_canary/archive.sqlite.gz`。哨兵只有测试文字，不是业务数据库。

已补上压缩 SQLite 备份及嵌套备份目录的排除规则，后端已重建；最终双镜像逐文件及 SQLite 文件头扫描尚未取回，所以此检查仍阻塞。不能仅凭 `.dockerignore` 修改宣称镜像已完全干净。

证据：[首次实际镜像扫描](image-exclusion-initial.json)、[最终源文件清单](build-source-manifest-final.json)。

## 5. 生产数据库是否实际验证

**是，已于北京时间 2026-09-09 11:48 左右取得实际证据，检查时健康；当前再次访问受 SSH 握手故障阻断。**

- Docker Compose v1.29.2，项目 sageai，部署目录 `/opt/sageai`。
- 实际数据库 SQLite，环境变量 `sqlite:////app/data/app.db`。
- 实际卷 `sageai-db-data`；容器路径 `/app/data/app.db`；宿主路径 `/var/lib/docker/volumes/sageai-db-data/_data/app.db`。
- SFTP 只读获取主文件、WAL、SHM，两次完整字节及元数据采集一致；在隔离复制品连同 WAL 上执行检查。
- integrity_check=ok、quick_check=ok、foreign_key_check 无错误；13 张表全部可读，task_record 11 条、record 2 条、user 4 条；报告引用缺失 0，四个本地损坏 UUID 均不在生产任务表中。
- 生产与本地 app.db 没有当前文件/卷依赖关系，数据及哈希不同；不能因此推断任何未知的历史来源。
- 当前已记录版本 5.0.0，运行后端 image ID `sha256:a1954471f1473036a7dda7a1250b169a8be6b4b3bf0415ce8956a7e362523332`。部署目录无法解析 git commit，commit=UNKNOWN；没有伪造版本追溯信息。

生产前端既存 unhealthy 有直接证据：wget 访问 `[::1]:80` 被拒绝；已在待发布文件中修正 IPv4 地址，没有改线上容器。

随后构建重试期间 SSH 端口可连接但没有 banner；Windows OpenSSH 与 Paramiko 均复现。HTTP 首页仍返回 200，但这不能证明此刻所有业务正常。尚无法确认 SSH 故障是否与资源压力有关，**不把时间相关性当作根因**。

状态应同时保留：`PRODUCTION_DB_LAST_VERIFIED=HEALTHY`（上述采集时间），`PRODUCTION_DB_STATUS=UNKNOWN`（当前复核不可达），`PRODUCTION_ACCESS=SSH_BANNER_TIMEOUT`。没有证据称生产数据库损坏，也不承诺它此刻持续健康。

证据：[实际数据库与校验](production-database.json)、[部署配置](production-discovery.json)、[版本](production-version.json)、[既存前端健康故障](production-frontend-health.json)、[当前端口响应](host-response-probe.json)。

## 6–8. 三项门禁

| 门禁 | 判定 | 具体阻塞项 |
|---|---|---|
| CODE_RELEASE_GATE | BLOCKED | 前端重试最终构建结果、最终双镜像数据库排除、独立容器启动/migration/六类审查及持久化回归未取得通过证据。不是因为本地仅恢复 33 条就阻塞代码。 |
| DATABASE_SWITCH_GATE | BLOCKED | 四条业务记录仍不完整，未获数据缺口处置确认；14 个历史报告引用的保留/清理策略未决定；没有执行切换。 |
| PRODUCTION_DEPLOY_GATE | BLOCKED | CODE_RELEASE_GATE 未满足；SSH/主机当前运维状态需要恢复确认，发布前须复核目标卷和数据库。上次健康生产快照是有效证据，但不是跳过当前发布验证的理由。 |

## 9. 必须人工决定或协助的事项

1. 四条任务逐条的数据缺口处置：继续保留独立残缺证据，是否接受恢复库缺失完整业务内容；本报告不建议未经确认删除。
2. 本地 14 个历史报告引用是否保留审计记录、清理引用或生成明确标注的派生报告。该决策与部署到健康生产库分开。
3. 通过云控制台确认主机内存/OOM、sshd 与本次隔离验证负载，恢复 SSH 或提供独立测试主机。已向用户请求该信息。不能用人工“接受风险”替代尚未通过的 Docker 技术检查。

## 10. 下一步最小动作

先从云控制台核实并恢复 SSH，取回 `/var/tmp/sageai-release-verify-20260909/build-result.json`、`build-frontend.log`、`runtime-result.json`。如需停止验证负载，只处理 `sageai-release-verify-20260909` 前缀的测试容器，以及已确认的本次 Vite 构建容器 `fa955a4a3df0`；不要操作生产服务。

访问恢复后先核对主机/生产容器状态，回收测试结果；如未通过，在足够资源的独立环境补齐构建、完整镜像扫描与业务回归，再重新计算代码/生产门禁。数据库切换仍单独等待数据处置决定。本轮不部署、不切库。

## 本阶段修改与保全

仅修改 5 个工程文件：

- `backend/main.py`：两处下载响应头对中文文件名进行 URL 编码，修复实测 HTTP 500。
- `backend/tests/test_download_headers.py`：三种格式 × 两个实际路由的中文文件名回归。
- `.dockerignore`：修复实际发现的压缩 SQLite 备份排除缺口。
- `Dockerfile.frontend`、`docker-compose.yml`：修复已确认的 IPv6 健康检查错误。

本阶段 17 项自动化测试通过；14 个历史任务详情/列表和 42 次导出通过，新报告三种导出通过。没有把 HTTP 200 当作历史正文完整恢复；原样保存的短报告仍只是原有内容。

本地 `backend/app.db`、`-wal`、`-shm` 的大小、mtime、SHA256 均与本阶段开始完全一致；候选数据库也保持不变。其他 12 张表既有逐字段一致的证据未被改变。原库物理损坏结构已证实，但导致该结构损坏的具体写入事件仍未证实。

证据：[本阶段开始](source-before.json)、[结束复核](source-after.json)、[自动化测试](pytest-results.xml)。
