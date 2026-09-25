# SQLite 备份、恢复候选与切换

## 约束

备份使用 `backend/sqlite_maintenance.py` 的 SQLite backup API，读取包含已提交 WAL 的一致快照；不再直接复制在线主文件。目的文件必须不存在，且不得带旧 WAL/SHM/journal；校验失败不会发布备份。保留备份的期限由运维决定，不自动删除。

`rollback.sh backup` **只校验并生成新候选文件**，不停止服务、不覆盖数据库、不自动选择最近备份、不执行切换。需要数据库切换时走下述人工流程。

## 安全备份与候选暂存

Compose 默认读取运行容器内实际 `DATABASE_URL`，输出到相同持久卷的 `/app/data/backups`：

```sh
bash backup.sh
```

非 Compose 环境须指定已核实的真实路径：

```sh
MAINTENANCE_MODE=local DB_PATH=/verified/path/app.db BACKUP_DIR=/verified/backups bash backup.sh
```

暂存指定备份到**新的**文件路径；Compose 模式路径均为容器内路径：

```sh
BACKUP_FILE=/app/data/backups/reviewed.sqlite RESTORE_OUTPUT=/app/data/candidates/reviewed-v1.db bash rollback.sh backup
```

本地模式另外设置 `MAINTENANCE_MODE=local`。支持普通 SQLite 与 `.gz`，损坏备份和已存在的目的文件会被拒绝。暂存只说明物理完整性通过，不代表业务数据齐全或获准切换。

## 环境要求

- 生产 SQLite URL 必须为绝对路径，明确指向持久卷。文件不存在时默认拒绝启动；只有首次部署并明确准备建立新库时才设置 `ALLOW_DATABASE_INITIALIZE=true`，初始化后移除此开关。
- 历史 006 迁移默认不随服务启动执行。确需执行时应在已确认的部署窗口设置 `RUN_STARTUP_MIGRATIONS=true`；执行后移除开关。不能通过普通服务重启隐式改变 schema。
- Docker 默认主库 `/app/data/app.db`，辅助库由 `SAGE_DATA_DIR=/app/data` 管理；Compose 使用命名卷 `sageai-db-data`。部署前必须检查实际 mount，不能凭仓库配置推断线上状态。
- pytest 自动创建 `sageai-test-*` 临时目录并设置 `ENV=test`、独立 DATABASE_URL、辅助库和日志路径。测试数据库导入若指向目录外则直接失败。独立验收实例也必须显式设置这些变量。
- `/health` 和 `/api/health` 在主库或关键表不可读时返回 503。启动做完整性检查，每个 worker 在健康请求触发时最多每 60 秒做一次 quick_check；每次只补充关键表首尾记录探测。该检查不能识别业务历史数据的完整性，例如未声明外键的旧报告引用。

## 切换前必须满足的条件

1. 明确是哪一个环境、哪个进程、哪个真实路径需要修复，核实生产数据库类型、卷、integrity_check、task_record 是否同样损坏。
2. 确认数据缺口处理：本轮 37 个已知任务中仅 33 条完整，4 条只有 id/task_id；14 个既有任务引用的报告 1 不存在。不得用占位数据假装完整恢复；旧报告引用可能来自历史删除，未经业务确认不得复活。
3. 验收候选 schema、索引、外键、逐字段差异与业务回归。云模型、真实客户凭据、Linux/Docker 实际构建与多 worker 部署验收另行完成。
4. 比较最新现场与本轮保全的哈希及 WAL 状态。如有新写入，必须重新保全、提取增量并重做核对，不能直接切换本轮旧快照。
5. 4 条不可恢复任务的数值 id 可能被普通 INTEGER PRIMARY KEY 后续分配重新使用。保留独立的 id/task_id 对照证据；切换前确定接受丢失后的编号策略，不能将新建测试记录误认为旧记录恢复。

## 停机、切换和回滚步骤（本轮未执行）

1. 另行批准停写窗口与明确的候选文件。入口停止接收新任务，等待所有 worker 和后台写入结束，保全所有主文件、WAL/SHM、配置和哈希。
2. 优雅停止旧实例可能触发 SQLite checkpoint；这属于后续需授权的操作。当前“原库不动”的约束下，本轮没有停止旧实例。
3. 将审核通过的候选放入同一持久卷中的**新版本路径**，校验哈希/完整性/权限。不要覆盖旧 app.db，不要把旧文件的 WAL/SHM 配给新候选。
4. 修改新实例的绝对 DATABASE_URL 指向新版本路径，先启动一个 worker，核实运行时 database_list/open-files/volume，再做登录、任务、报告、重启和健康检查。检查通过才恢复入口流量，再验证多 worker。
5. 切换后留观察窗口及新库安全备份。若出现故障，立即停写并保全新库增量；回滚代码必须继续指向经验证的数据库路径。
6. **旧 app.db 已知损坏，不能把指回旧库称为安全回滚。**没有另一份已验证、数据窗口可接受的健康库时保持维护模式，处理新写入与候选问题；不能丢弃切换后的新数据来强行回退。

## 当前发布结论

本轮 `release_quality_gate = BLOCKED`。候选物理结构和已覆盖的独立实例回归通过，但任务与历史关联缺口尚未获业务确认，生产实际库与 Docker 构建尚待核验；没有执行正式切换。现场主文件保持字节不变，但运行服务的 WAL/SHM 在本轮期间发生变化，包含 4 个索引增量；已在副本中重放、核对并生成 `artifacts/db_recovery/candidates_latest`。业务行未发现增量，但不能声称整个在线库状态完全未变。

SQLite 官方说明：恢复可能找回旧数据、改变字段或表归属，因此必须做业务核对，不能只看 integrity_check。[恢复文档](https://www.sqlite.org/recovery.html)。在线一致快照采用官方备份机制。[Backup API](https://www.sqlite.org/backup.html)。
