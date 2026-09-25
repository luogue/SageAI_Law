# backend/app.db 只读诊断报告

日期：2026-09-09。结论基于工作区代码、本机运行进程、SQLite 只读检查、已有日志和本地备份来源。**未修复、重建、删除或覆盖数据库；未执行 dump、recover、VACUUM、checkpoint、migration，未重启服务。** 本次仅新增本目录的诊断脚本、统计和报告。

## 1. 结论

- `backend/app.db` 是**当前本地应用正在使用、含账户和历史业务记录的默认业务库**。开发联调正在使用它；不能称为可丢弃测试库，也不是仅历史兼容遗留。
- 已确认 `task_record` 表的 B-tree 结构局部损坏：根页 26 指向不存在的页 94，并引用了同时列入 freelist 的页 69。不是文件头错误，也不是整库不可读。
- 37 个任务 ID 的索引条目仍可读取。逐条完整 SELECT 验证：任务行 ID 1–33 可读，34–37 报 SQLITE_CORRUPT。其余 12 张表的全表读取和逐表 integrity_check 均通过。**4 条任务有明确的数据不可读/丢失风险，不能保证恢复。**
- 当前本地旧版任务持久化、启动恢复和部分历史任务查询已受影响；不仅是历史数据库检查失败。任务恢复错误最早见于现存日志的 **2026-08-28 09:10:19**，早于画像修改。
- V2 同步审查引擎、画像配置和画像归一化不读写 `task_record`；不能将此故障等同为画像修复失效。但使用该坏库的环境**不能通过完整业务发布验收**。
- 仓库 Docker Compose 指定另一物理数据库——命名卷 `sageai-db-data` 内 `/app/data/app.db`。**生产实际挂载和完整性尚未核实**：已尝试严格主机校验、非交互只读 SSH 查询，认证被拒绝，远端命令未执行。不能无条件宣布生产不受影响或批准发布。

## 2. 数据库用途：配置与运行时证据

| 证据 | 说明 |
|---|---|
| `backend/storage/database.py:14` | `DATABASE_URL` 缺省为 `sqlite:///./app.db`，相对于进程工作目录，不相对于源码文件。 |
| `backend/.env` 的 DATABASE_URL | 本地配置同样为 `sqlite:///./app.db`，仅读取数据库配置，未记录其他敏感环境变量。 |
| 当前 PID 10296 | Python/uvicorn，cwd=`F:\ai\Sage\backend`，环境 DATABASE_URL=`sqlite:///./app.db`，监听 8016。 |
| 当前进程文件句柄 | 实际打开 `F:\ai\Sage\backend\app.db`、`app.db-wal`、`app.db-shm`。这是运行时证据，不是按文件位置推测。 |
| `frontend/vite.config.js` | 开发代理指向本地 8016；前端进程监听 5173。 |
| `scripts/run_basis_live.py:8`、`:12` | 切入 backend 并按现有本地登录账户读取该库，用于真实前端代理联调。 |
| 当前数据 | user=1、admins=1、record=1、feedback=1、admin_logs=9、security_events=31，以及 37 个任务索引条目。无法仅凭这些数据断定账户属于真实客户或测试人员，所以不允许按测试库丢弃。 |
| `docker-compose.yml:20`、`:25`、`:77` | Compose 显式 URL=`sqlite:////app/data/app.db`，挂载命名卷 `sageai-db-data`。若线上严格使用此配置，本地 backend/app.db 并非该数据卷中的业务库。 |
| `.env.production` / 示例 | URL=`sqlite:///./data/app.db`；Compose 显式环境变量优先且使用绝对路径。脱离 Compose 的启动方式须另核实 cwd 和真实 URL。 |

生产仍依赖 SQLite 业务数据库，只是不应依赖本机这份损坏文件。**没有证明当前生产容器确实按上述配置运行，也没有检查到生产卷的数据。**

## 3. 只读检查结果

检查使用独立 Python sqlite3 与 sqlite3 CLI，URI 为 `mode=ro&immutable=1`，不导入应用 main/storage 初始化。immutable 检查忽略 WAL；本次 WAL 长度为 0，主文件与侧文件在每次检查前后哈希和元数据一致，检查期间未观察到内容变化。该方法不能泛用于持续写入、有未合并 WAL 的在线库。参见 [SQLite URI 文档](https://www.sqlite.org/uri.html)。

| 项目 | 结果 |
|---|---|
| 文件大小 | 344,064 bytes，336 KiB |
| 创建时间 | 2026-05-30 23:11:19 UTC（北京时间 05-31 07:11:19） |
| 最后修改 | 2026-08-29 00:13:54 UTC（北京时间 08-29 08:13:54） |
| SHA-256 | `0986b6e7fbda02db9f73213bcea0df75e36458274951101d649a9bfca53e80cf` |
| SQLite 文件头 | `SQLite format 3\0` 合法；page_size=4096 |
| 页数 | 声明 84，物理 84，无尾部余字节，无全零页 |
| 文件格式 | read_version=2、write_version=2，WAL 格式；文件头记录最后写入 SQLite 3.40.1 |
| integrity_check / quick_check | 均失败。CLI 3.44.3 返回 SQLITE_CORRUPT（11）；Python sqlite3 同样复现。 |
| schema | 13 表、23 索引可读；task_record 根页为 26。 |
| WAL | 存在，0 bytes；无可用 frame。 |
| SHM | 存在，32,768 bytes；它是共享索引，不是丢失数据页的完整备份。 |
| rollback journal | 未发现 app.db-journal。 |
| dbstat | 当前 Python SQLite 未编译该虚表；改用逐表完整性检查、独立 CLI 和原始 B-tree 页头解析定位。 |

CLI 原始错误：

```text
Tree 26 page 26 cell 0: invalid page number 94
Tree 26 page 26 cell 7: 2nd reference to page 69
Error: stepping, database disk image is malformed (11)
```

原始页解析进一步显示：第 26 页为内部 table B-tree 页，最右子页指针为 94；第 7 个分隔单元指向第 69 页。freelist 实际包含 69、70、71、72、73、81、82。因此页 69 的重复引用与页 94 的越界不是 UI/ORM 文案问题或索引重建即可保证解决的问题。

逐表结果：

| 表 | 完整读取数量 | 逐表完整性 |
|---|---:|---|
| user | 1 | ok |
| admins | 1 | ok |
| record | 1 | ok |
| feedback | 1 | ok |
| admin_logs | 9 | ok |
| security_events | 31 | ok |
| blacklist、bonus_log、file_hash_cache、intercept_logs、invite_rewards、reward_logs | 各 0 | 均 ok |
| task_record | 全扫描中断；按主键分别读取可读 33 条、失败 4 条 | malformed |

task_record 的可读数据来自 2026-06-11 至 06-14；不输出合同、手机号、密码、任务正文。索引中的 37 条不代表一定恢复了 37 条完整记录。逐表通过也不代表损坏库继续写入是安全的；本次没有进行写入验证。

## 4. 根因判断：已证实与尚未证实

**已证实的直接原因**：任务表页引用、文件页集合和空闲页管理不一致。页 94 不在文件中，页 69 同时被当作活动子页与空闲页。

**操作层面的确切原因尚不能确定。** 当前最应优先排查的是非一致性的文件复制/覆盖/恢复、主库与日志文件错配或日志丢失，导致不同事务时点的页面混合。页数对齐且头部声明也为 84，使“单纯从尾部截短、其他内容完全未变”的解释不充分。WAL 为空只是现状，不是证明它曾被删除的证据。

SQLite 官方指出，事务期间直接复制文件会形成混合时点快照，丢失或错配热日志也会破坏恢复能力；这些机制与现象相符，但仓库存在危险脚本**不等于证明该脚本已对本库执行过**。[SQLite 损坏原因说明](https://www.sqlite.org/howtocorrupt.html)

其他检查：

- 已有日志共命中 1,187 行 malformed（可能含多份日志的重复记录），最早为 `backend/logs/app_2026-08-28.log:3`。mtime 晚于最早错误，不能用 mtime 当作损坏发生时间。
- 系统日志存在 06-20、08-01、08-04 的非正常关机记录；没有证据将某次关机与具体数据库写入关联。F: 为本地 NTFS，08-27 的 NTFS 事件报告 F: 健康；所查期间未发现选定磁盘/文件系统错误事件。没有运行磁盘修复或硬件压力测试，不能完全排除硬件问题。
- `WAL + synchronous=NORMAL` 并不能单独解释结构损坏：SQLite 文档说明该组合保持一致性，但系统崩溃/断电可能丢失最近提交的持久性。不能把 NORMAL、普通进程退出或多线程本身当作已证实根因。[SQLite synchronous 文档](https://sqlite.org/pragma.html#pragma_synchronous)

## 5. 代码层风险

| 模块 | 发现 | 判断 |
|---|---|---|
| `backend/storage/database.py` | check_same_thread=False、WAL、NORMAL、busy_timeout=5000；每次连接设置 PRAGMA；未找到显式 checkpoint 或关闭 autocheckpoint。 | 默认自动 checkpoint 并非错误；跨线程允许不等于已发现连接被同时共享。不要为诊断运行 checkpoint。 |
| `Dockerfile.backend` / `backend/main.py` | 生产配置 6 worker；旧版有后台进度线程及 asyncio.to_thread，多个会话可并发写任务。当前本地只观察到一个打开目标库的后端进程。 | 增加写竞争，通常应由 SQLite 锁协调；未发现使用 --preload 继承已打开连接的配置，不能直接归因为多进程。 |
| `backend/tasks.py:56` | 每次持久化新建会话，正常 commit，异常 rollback/close；内存先更新，DB 失败只记警告。 | 生命周期相对完整，但会掩盖数据未落库；返回成功后重启可能丢失内存任务。 |
| `backend/tasks.py:119`、`:172` | 启动恢复整批查询失败被捕获为“可能表尚未创建”；单任务失败返回 None。 | 确认损坏被误报/隐藏，API 可能表现为任务不存在，而非明确存储故障。 |
| `backend/storage/crud.py`、`backend/routers/admin.py` | 大量 `db = next(get_db())`；生成器生命周期没有被调用方管理。多数写函数没有统一异常 rollback/finally close。 | 临时生成器可能在真正查询前被关闭，Session 后续又可获取连接，实际使用后的释放不确定。需要修复，尚不能证明导致物理坏页。 |
| `backend/main.py:105` | import main 即 create_all、恢复任务；dotenv 加载与数据库模块导入存在顺序耦合。 | 未发现 create_all 覆盖既有数据库文件；但相对路径+CWD 或错误 env 可创建/使用另一个空库。 |
| 测试 | `test_security.py` 使用真实 init_db/CRUD；`test_legacy_review_fallback.py` 导入 main 并 create_task；未找到集中配置临时 DB 的 conftest。 | 测试若继承业务 DATABASE_URL，或从 backend 启动，会使用同一个库。风险已确认，未执行这些测试。 |
| `backup.sh:12`、`:27` | 默认取宿主机 backend/data/app.db，直接 cp 主文件，不建立 SQLite 一致性快照。 | 热备方式不安全，并且与 Compose 命名卷路径不一致，可能备份错库。 |
| `rollback.sh:68`、`:74` | 同样恢复宿主机 backend/data/app.db，而非明确解析实际生产卷；没有完整性/数据差异验证。 | 可能恢复错库；不能作为现成可靠恢复流程。 |
| `.dockerignore`、`Dockerfile.backend:21`、打包脚本 | 未排除 *.db、*-wal、*-shm。Docker COPY backend/ 会将本地数据库一起放入镜像；打包也会包含它们。 | Compose 下 `/app/app.db` 与业务卷分开，但错误/独立启动可使用镜像中的坏库。应在发布前消除打包风险。 |
| `build_deploy.py:56` | 部署会删除远端 backend/frontend 再解包；默认备份脚本却指向 backend 下的库。 | 对脱离命名卷的部署存在数据被替换风险；无证据证明本地损坏由此造成。 |
| migrations / Alembic | 004 默认 sql_app.db，005/006 硬编码 data/app.db，其余用 ORM URL。001 upgrade 从 storage.database 导入并不存在的 init_db；downgrade 为 drop_all。 | 多套目标路径不一致；迁移不恢复业务数据，现成迁移流程也不能不经验证直接运行。 |
| `backend/main.py:1510` | Docker 使用的 /health 固定返回 healthy，不检查 DB。 | 服务能启动且显示健康，不能证明任务数据库正常。 |

## 6. 功能和发布影响

| 功能 | 当前结论 |
|---|---|
| 旧版合同审查任务 | 计算可继续在内存中发生，但持久化、重启恢复、损坏行历史查询有真实故障；不能保证完成状态/报告关联持久化。 |
| 任务列表/状态 | 列表取内存；启动恢复失败导致旧任务缺失。损坏行 DB fallback 失败可返回“任务不存在”。 |
| 用户/管理员/额度/历史报告/反馈 | 对应表当前读检查通过，没有发现这些表的结构损坏；登录及业务功能仍依赖该业务库。未做写入测试，不承诺坏库上的后续写入正常。 |
| V2 同步审查 | `/review-v2/file` 与 `/checklist` 未调用 TaskRecord、create_task 或 create_record；引擎按请求计算。鉴权依赖验证 token，登录取得 token 则依赖 user 表。安全中间件另有数据库/缓存依赖。当前 task_record 损坏不是 V2 计算的直接依赖故障。 |
| 用户风险画像 | 无专用数据库画像表；配置在代码，状态在请求中，未发现本库损坏污染画像配置。 |
| 配置 | 核心配置来自环境变量/文件；该 SQLite 库并非配置库。 |
| 本地完整版本验收 | **阻塞**：当前活动库完整性失败、任务恢复已失败；不能以 V2 专项测试通过或 /health healthy 作为整套业务放行。 |
| 画像代码在独立健康生产库发布 | **不构成必然阻塞，但目前不能无条件放行**。须核实线上真实 URL/卷、只读完整性、可靠备份及打包隔离；SSH 认证失败留下未核验项。 |

本次没有发送审查/登录/写入 API 请求来验证故障，避免触发余额、任务、审计或其他业务写入。影响结论来自静态调用链、原始只读 SQL 和现有运行日志。

## 7. 恢复来源

| 来源 | 检查结果 | 可用性 |
|---|---|---|
| backend/app.db-wal | 0 字节 | 无 frame 可补回页 94。 |
| backend/app.db-shm | 32 KiB | 不是完整数据备份，不应尝试用它替换缺页。 |
| 项目内 .bak / .sqlite(.gz) / 备份归档 | 未找到 | 本地未找到可直接恢复的业务备份；未覆盖任何文件。 |
| 根目录 app.db | 完整性 ok，但 user=0、record=0、task=5，schema 亦有差异 | 独立状态，不能覆盖当前含账户/历史数据的库。 |
| backend/data/app.db | 完整性 ok，仅 admin_logs/security_events/sqlite_sequence | 不是当前业务库的完整备份。 |
| backend/pipeline_test.db | 完整性 ok，业务表为空 | 只能参考结构，不恢复业务行。 |
| artifacts/company_formation/baseline/backend/app.db | 完整性 ok，业务表为空 | 同上。 |
| artifacts/employment_round2_snapshot/app.db | 完整性 ok，业务表为空 | 同上。 |
| ORM/migration | 可以用于核对表定义，存在上述迁移缺陷 | 不能恢复账户、报告、任务的原始数据。 |
| 现有 logs / artifacts / .runtime-logs | 用 4 个损坏任务索引中的 task_id 检索，未命中 | 未找到这 4 条完整任务的外部副本。 |
| 生产卷/异地备份 | SSH 认证失败，尚未检查 | 有无可用备份未知，不能假设存在或覆盖恢复。 |

## 8. 推荐方案与审批边界

**推荐 A：保全证据后，在独立目录恢复候选库并验收，最后另行批准切换。**

1. 先明确允许的停写窗口。当前库仍被运行进程打开；停止服务可能触发 SQLite 的正常清理/检查点，必须在批准后按保全顺序处理，不能随意 kill 或删除侧文件。
2. 在批准的停写/一致性保全流程中，保存原 DB/WAL/SHM 的原样副本、哈希、元数据和日志；保留原库不覆盖。
3. 仅对隔离副本尝试 SQLite 恢复到**新的候选库**，并与逐主键可读数据、37 个索引条目、schema、用户/报告关联逐项核对。恢复不能保证找回物理缺失页；不静默丢弃 ID 34–37。
4. 对候选库运行完整 integrity_check、foreign_key_check、数量与业务关系核验，在独立测试环境验证登录、额度、记录、任务创建/查询/重启恢复以及 V2 审查。
5. 提交恢复清单、不可恢复清单、数据差异、回滚步骤，**再次确认后才切换实际业务库**。

风险：保全与隔离检查低风险；从损坏文件生成候选库中风险；正式替换中高风险；4 条任务的数据丢失风险仍然存在。整个方案不能称为“无损修复”。在线备份应使用 SQLite 一致性备份机制，而非直接 cp。[SQLite Backup API](https://www.sqlite.org/backup.html)

备选 B：若找到经过校验、属于同一业务实例的真实备份，先恢复到隔离候选库，比较备份时间和增量损失后再批准切换；风险中高。当前没有这样的已验证备份。

不推荐 C：删除/重建空库。会丢失至少已知账户、报告、反馈和可读任务，风险高；**未获授权，不执行**。

## 9. 后续代码修复建议（本次未修改）

需要后续修复，建议单独确认实施范围：统一绝对数据库路径与 env 加载；测试使用临时独立库并防误连；统一 Session/事务上下文；损坏与锁冲突分类报错，持久化失败不得伪装成功；DB readiness 检查；一致性备份和实际数据卷恢复；部署排除 DB/侧文件；修正迁移路径和初始迁移函数引用。多 worker 下内存任务/信号量各自独立的问题也应纳入任务存储设计检查。

涉及主要文件：`backend/storage/database.py`、`backend/storage/crud.py`、`backend/tasks.py`、`backend/main.py`、`backend/routers/admin.py`、`backend/tests/test_security.py`、`backend/tests/test_legacy_review_fallback.py`、`backend/config.py`、`backend/migrations/*`、`backend/alembic/versions/001_initial.py`、`backup.sh`、`rollback.sh`、`.dockerignore`、`Dockerfile.backend`、`docker-compose.yml`、`build_deploy.py`、`deploy_to_server.ps1`。

## 10. 本次诊断产物

- `readonly_probe.py`：不导入应用、immutable 只读 SQLite 检查脚本。
- `readonly-results.json`：六份本地数据库的结构、完整性、汇总扫描和前后哈希。
- `native-checks.json`：独立 CLI 的 integrity/quick_check 原始输出、哈希和生产认证失败记录。
- `page-and-row-diagnostics.json`：根页/空闲页关系、37 行逐主键可读性、逐表完整性。
- `runtime-and-history.json`：当前数据库句柄与早期损坏日志位置。
- `recovery-source-search.json`：4 条损坏任务的外部副本检索结果。

没有修改应用源码、测试、配置、部署脚本或任何数据库文件；下一步停写、恢复候选库、切换与防复发代码修改均等待用户确认。
