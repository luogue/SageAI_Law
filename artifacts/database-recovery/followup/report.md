# 数据完整性追查与切换决策（2026-09-11）

**SAFE_TO_SWITCH=NO**。未合并任何数据，未切换或改写正式库，未修改健康检查。

## 来源与范围
扫描目录 171439 个，候选文件 11202 个。根目录：F:/, D:/, E:/, G:/, H:/, M:/, N:/, C:/Users/Administrator, C:/ProgramData。
检查项目根库、原库保全副本、WAL重放副本、旧测试快照、临时目录备份；候选检查文件含45份业务表数据库结果及1条无法读取记录。完整性失败的原库副本保留损坏结论，不认定为完整备份。
旧服务器通过现有受信SSH连接只读检查 /opt/sageai 及 Docker 卷。/opt两份库无目标表，pipeline_test为空；业务Docker卷有11条任务、2条报告，验收卷有1条任务、1条报告，均integrity_check=ok，但目标UUID匹配数为0。
所有5743份ZIP尝试检查目录，未找到app.db/相关目标成员；其中105份目录读取报错。75份名称相关的压缩包检查记录另存，唯一含数据库成员的是发布排除测试canary，不是历史业务数据。303份SQL/dump扫描目标UUID无命中。
限制：96处访问失败/失效路径；跳过系统、依赖及缓存目录（完整名单见inventory.json）；未对全部无关RAR/7z及大型软件归档解包，未检查未挂载、离线或未知云备份。因此不能宣称永久不可恢复。

## 合并结论
补回任务0条，补回目标历史报告0条。匹配不到业务UUID的同号记录、验收生成报告均拒绝合并。
恢复库内33条任务及其他12张表44条完整记录未变；候选SHA256与上轮验证一致。
关键歧义：14条任务引用同一个数值report_id=1，但日志记录了14次成功删除并存在编号复用。它们不能被视为同一报告，也不能把任何备份中的record.id=1赋给全部任务。恢复必须核对任务UUID、trace、创建时间、用户、原文件身份与报告内容。

## 4条不完整任务（未证明永久丢失）
|ID|task_id|缺失与影响|
|---|---|---|
|34|c6daf70a-ed9c-443a-9ad6-0b742f51ce76|数据库完整行不可读；日志可补部分身份字段，但结果、metadata、validation、summary、进度、错误及数据库时间未可靠恢复。历史报告3亦未补回，详情/报告不可完整查看。|
|35|7ea566e9-1f67-4d2e-bceb-a88c405081be|数据库完整行不可读；日志可补部分身份字段，但结果、metadata、validation、summary、进度、错误及数据库时间未可靠恢复。历史报告4亦未补回，详情/报告不可完整查看。|
|36|89ff9724-8eb3-43c5-8169-6071a0ba2bdc|数据库完整行不可读；日志可补部分身份字段，但结果、metadata、validation、summary、进度、错误及数据库时间未可靠恢复。历史报告4亦未补回，详情/报告不可完整查看。|
|37|e451edda-230a-49f9-8c23-7668892fb607|数据库完整行不可读；日志可补部分身份字段，但结果、metadata、validation、summary、进度、错误及数据库时间未可靠恢复。历史报告4亦未补回，详情/报告不可完整查看。|

## 33条可读任务的逐条报告状态
AVAILABLE表示关联报告存在；NO_REPORT_REFERENCE不等于报告丢失；MISSING_REFERENCED_REPORT表示任务可读但所引报告不可用。
|任务ID|task_id|record_id|报告状态|
|---|---|---|---|
|1|039246e1-87b7-4a2d-ac5c-dcdc232da032|None|NO_REPORT_REFERENCE|
|2|21164666-2fde-42f8-bf1c-0d3cf817f2e3|1|MISSING_REFERENCED_REPORT|
|3|e1979315-39d9-4c7d-9045-0b7d01421f7f|1|MISSING_REFERENCED_REPORT|
|4|a0d4f1de-b0fd-4e3a-8f96-a3f899eac160|2|AVAILABLE|
|5|c54d9a43-815d-4ff4-bf29-acd54814493a|1|MISSING_REFERENCED_REPORT|
|6|a85efd56-be59-42d3-b805-372fa9b0eff6|1|MISSING_REFERENCED_REPORT|
|7|1bd4519f-e0fa-4171-9982-1168c6584e3b|1|MISSING_REFERENCED_REPORT|
|8|4033339b-d079-460c-8158-5021b60c7f7b|1|MISSING_REFERENCED_REPORT|
|9|fa2f9351-2fcb-4fdb-a728-f08553f41a70|1|MISSING_REFERENCED_REPORT|
|10|5f5eb1ca-bf3c-4351-8a62-3222456fc3ec|1|MISSING_REFERENCED_REPORT|
|11|14ddcac1-9428-4ab4-a9e5-195f8427ea81|1|MISSING_REFERENCED_REPORT|
|12|98d8b82d-136f-49f3-8ce5-5fb469077f46|1|MISSING_REFERENCED_REPORT|
|13|c52b5ff0-6ffc-4329-9786-2d702ba78cd0|1|MISSING_REFERENCED_REPORT|
|14|23f1a55f-8a73-4de4-a245-12a9ca334e66|None|NO_REPORT_REFERENCE|
|15|6158f349-5c32-4351-a1c9-7552647fca44|None|NO_REPORT_REFERENCE|
|16|bc3f13f0-64f6-4150-b511-e41a22b75d53|None|NO_REPORT_REFERENCE|
|17|8a3bdc71-e406-4b0b-9b0c-88695f9854b2|1|MISSING_REFERENCED_REPORT|
|18|cf59c42a-30c1-4cc3-bd1b-64f21aa9d33a|None|NO_REPORT_REFERENCE|
|19|24ae90ee-85a6-47b1-8aaf-931b832b7c33|None|NO_REPORT_REFERENCE|
|20|2e04712c-1275-469f-a38d-cef2c470786e|None|NO_REPORT_REFERENCE|
|21|fea66ee0-065d-45a0-88e7-4a1dbad2b095|None|NO_REPORT_REFERENCE|
|22|ce4533c6-c083-4620-8e45-c974fe21840c|1|MISSING_REFERENCED_REPORT|
|23|96c81b88-aed6-4f86-adda-779cf2905dc1|None|NO_REPORT_REFERENCE|
|24|e9a03e38-d004-4071-a90e-eab1487a2915|None|NO_REPORT_REFERENCE|
|25|a4886db4-ee75-43eb-a686-4f50b9ad3341|None|NO_REPORT_REFERENCE|
|26|cbe57f96-7856-448d-b494-dff19c6ad1a2|1|MISSING_REFERENCED_REPORT|
|27|13f2f19f-6fae-4851-8d49-5e58d37419db|None|NO_REPORT_REFERENCE|
|28|75b9efdc-224a-40ee-be94-2e2e6068b248|None|NO_REPORT_REFERENCE|
|29|2a9778a0-70e5-406a-8299-b51ea2c3975d|None|NO_REPORT_REFERENCE|
|30|132c7e96-3948-4328-9e21-6f477a5484b9|None|NO_REPORT_REFERENCE|
|31|3c8911cf-0ca9-47ac-bccd-bc1e548f8e99|None|NO_REPORT_REFERENCE|
|32|4dd43986-00d4-443e-86b6-1e0e2c0e0730|None|NO_REPORT_REFERENCE|
|33|496c98dc-09f8-475c-a6d8-bf8dd1a8ffe0|2|AVAILABLE|

## 验证
本轮只读复验 integrity_check=ok，foreign_key_check无异常；业务层14条悬空报告引用依然存在（该列未声明外键，所以外键检查ok不能证明引用完整）。
没有合并/改动，因此未重复执行写入测试；上轮相同哈希候选的任务CRUD、33条历史读取及4线程24次并发验证仍适用。
正式主库哈希与停机备份一致；恢复库哈希：6aa516ed8aeebf6b1501ce6339e37a5870813600ed8ac1f9f346237b8b32ccf6。健康检查仍HTTP503，未伪装正常。

## 接受缺口后的条件式切换方案（未执行）
1. 业务方逐项确认接受4条不完整任务、14条历史报告引用缺口，以及4条损坏任务另有关联报告3/4缺失；不是只接受一个总数。保留可追溯缺口清单，不补造报告、不复活已删除报告。
2. 在恢复候选副本上实现缺口展示和历史数值ID防复用，保护34–37及已删除报告编号，另行验证；不能仅设置当前最大ID后继续使用会复用编号的旧机制。
3. 安排停写窗口，停止所有相关写入进程；再备份正式DB/WAL/SHM与配置，核对停机后增量。只合并确认的新记录，冲突则停止。
4. 再验完整性、逐字段差异、主键/业务引用、CRUD、历史读取、并发；数据缺口须与已接受清单完全一致。满足后方可改判SAFE_TO_SWITCH=YES。
5. 使用新的绝对DATABASE_URL指向已验收新库；保留原库原路径，不原地覆盖。启动后核实实际路径和哈希，先只读/限制写入进行冒烟验证。
6. 若切换失败，停止新实例，保全新库及其WAL/SHM，恢复原配置。原库仍损坏，回滚仅恢复原服务状态，不是恢复健康；若新库已产生写入，必须先保全并对账新增数据，禁止直接切回丢弃新增记录。

目前缺口未被用户接受，且存在尚未排除的备份来源限制，结论保持NO。