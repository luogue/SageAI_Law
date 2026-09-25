# 数据库独立验收（2026-09-11）

状态：恢复库结构检查通过；数据完整性仍有缺口，未切换正式库。

## 根因与范围
实际数据库：F:/ai/Sage/backend/app.db。task_record 根页26引用不存在的页94，文件和文件头均为84页，属于B-tree页结构损坏，不是单纯索引损坏。具体触发事件没有足够证据确定。现存日志最早错误：2026-08-28 09:10:19。
本次停机备份见 backup-path.txt 和备份目录 manifest.json。原库未覆盖。

## 恢复和验证
逻辑导出重建表及索引恢复33/37条任务；其余12张表44条记录逐字段一致，共77条完整记录。官方.recover --ignore-freelist结果同样仅33条任务。
integrity_check=ok，quick_check=ok，foreign_key_check无异常。全部33条历史任务可读；隔离副本使用实际tasks模块4线程并发完成24次新建、更新、查询、删除，结束后完整性ok。
本次数据与之前恢复候选逐字段一致。无新增已知损失；4条任务仍无法完整恢复。

## 不完整记录
以下日志字段仅为辅助取证，不冒充数据库完整行；未插入占位记录。
|表|主键|任务ID|无法从原库恢复字段|业务影响|
|---|---|---|---|---|
|task_record|34|c6daf70a-ed9c-443a-9ad6-0b742f51ce76|除id/task_id外15个字段|任务详情、结果和历史报告无法完整读取|
|task_record|35|7ea566e9-1f67-4d2e-bceb-a88c405081be|除id/task_id外15个字段|任务详情、结果和历史报告无法完整读取|
|task_record|36|89ff9724-8eb3-43c5-8169-6071a0ba2bdc|除id/task_id外15个字段|任务详情、结果和历史报告无法完整读取|
|task_record|37|e451edda-230a-49f9-8c23-7668892fb607|除id/task_id外15个字段|任务详情、结果和历史报告无法完整读取|

日志辅助证据另见 missing-record-details.json：可确认文件名、历史状态等部分信息，但 result、metadata_json、validation_json、summary_json、progress、error、created_at、updated_at 仍无可靠完整值。
另有14条任务引用缺失record_id=1，属于原有业务关联缺口，不能据此断言由本次页损坏造成，也不能假造恢复。任务id：2,3,5,6,7,8,9,10,11,12,13,17,22,26。

## 切换结论
不可以作为无损恢复库直接切换：4条任务及历史报告缺口未解决。保留原库、WAL/SHM、恢复候选及独立损失清单。需要完整备份补齐，或由业务方明确接受历史缺口后制定切换方案；不得将结构检查ok等同业务完整。
原服务已重新启动，仍使用原库，仅供现有合同链路继续测试，数据库健康检查应继续报错；不认定后端整体正常。
恢复候选：F:\ai\Sage\artifacts\database-recovery\recovered.db
SHA256：6aa516ed8aeebf6b1501ce6339e37a5870813600ed8ac1f9f346237b8b32ccf6