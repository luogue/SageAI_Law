# 正式数据库切换验收

SAFE_TO_SWITCH=YES
PRODUCTION_DB_SWITCHED=YES

范围：本机 F:/ai/Sage/backend 业务实例（127.0.0.1:8016）。未切换旧服务器或其Docker数据卷。

配置切换时间：2026-09-11T10:28:24.717336+08:00
全部业务验收完成：2026-09-11T10:30:12.244237+08:00
新后端PID：22520；backend/.env持久设置绝对DATABASE_URL。

## 原库保留
原位置：F:\ai\Sage\backend\app.db
最终备份：F:\ai\Sage\artifacts\database-switch\original-final-backup\app.db
大小：344064 bytes
SHA256：f5e6d39909b67672e881815e1669486d93984ad895cb2f18246c9b5c36f2eb9e
原位置及最终备份已设只读；未删除、未覆盖。备份含WAL、SHM及原配置。切换前健康状态HTTP503，详见pre-health.json。

## 新正式库
路径：F:\ai\Sage\backend\data\recovered-production-20260911.sqlite
验收后主文件SHA256：fab37791ea4675b822c0c9cc6def322e60cd788de01ea59b6d60dcf9dc37d14e
此哈希为验收时刻值，后续合法写入会改变。另保留一致性验收快照 accepted-production.sqlite，哈希 0f27d5205c3173e4aeceab752bac852b27d92610548e21a5d07e5cf351e27db4。
已验收恢复源哈希仍为6aa516ed8aeebf6b1501ce6339e37a5870813600ed8ac1f9f346237b8b32ccf6。上线副本仅增加AUTOINCREMENT、历史编号插入保护、独立recovery_data_gaps清单，全部77条原恢复数据逐字段一致；没有伪造缺失业务记录。

## 验收结果
- integrity_check：ok；foreign_key_check无异常。
- healthcheck：HTTP200 healthy / database ok，未改变健康检查实现或门槛。
- 任务创建、更新：实际生产repository；查询、删除：实际HTTP接口，全部通过。
- 33条历史任务可读；14条缺失报告关联按已接受清单保留。
- 4线程24次任务CRUD通过，测试任务已删除。
- 使用未修改小时制协议，经DeepSeek和业务POST /review-v2/file重新生成完整报告，HTTP200 / REPORT_READY。
- 实际生产create_record保存报告ID5，通过GET /api/records/5及独立repository重新读取，正文一致；报告SHA256：f04f5694c3fd40437ba18ba14f95a1e3a13a9aea23b125dc42952e6a99a7653f。这是本次新报告，不是历史缺失报告替代品，予以保留供验收。
- 报告1、3、4继续明确404；保留编号，禁止误关联。ResultPage对404显示明确不存在/无权访问提示，未暴露或假造旧报告。

## 已接受缺口
任务34–37无完整行；14条任务对应历史报告不可用（引用report_id=1的编号历史复用，不视为同一报告）。详细UUID、影响和历史状态见 ../database-recovery/followup/report.md 及新库recovery_data_gaps。
这些已接受缺口仍然存在，不能视为已补齐；不再阻止本次切换。未发现新的阻断级数据库风险。

## 回滚方案（未触发）
如出现完整性/健康/CRUD/报告读写/错关联异常：停止本机8016后端及相关写入；先保全新正式库和WAL/SHM、日志及切换后数据，不可丢弃报告5或其他新增记录；恢复original-final-backup/.env中的配置内容。原库仍是损坏状态且只读，回到原库不能承诺健康或写入成功；需要恢复原运行状态时应明确恢复写权限并维持异常健康提示。优先利用已验收的新库快照及已保全增量排障，禁止无对账直接丢弃新数据。旧库、旧备份永久保留，不纳入清理。
