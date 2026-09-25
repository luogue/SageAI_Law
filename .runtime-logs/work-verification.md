# 加工承揽路由与证据一致性回归

输入原件：test_data/56 承揽合同.docx，未修改。正常买卖原件：test_data/2 买卖合同.docx。

## 根因

1. domain_selection主要比较买卖、租赁、服务与技术合同，未对承揽角色和定作加工义务设置结构性优先识别。原材料采购及交付字段使买卖得分上升。
2. 原承揽规则以宽泛关键词召回，可能把物流公司的资质、原材料采购、付款或不可抗力条款当作对应工作义务。
3. 要素校验原先优先读取text，可能借用整段条款的内容支持一个不相关的quote；发布绑定也曾仅检查引文属于同一条款，没有重新核对对应要素。
4. 买卖的质保、检验、数量和生效事项缺少足够精细的源片段匹配；重新抽取证据时未同步更新旧evidence_location。

## 修改

- backend/review_v2/domain_selection.py：承揽角色与按定作要求加工的联合触发先于普通货物信号，加载work_contract规则。
- backend/review_v2/work_evidence.py：承揽44项原子要求；句级直接绑定；独立保留明示质保期限；保存统一源片段库。
- backend/review_v2/sale_evidence.py：稳定源ID；区分验收期限与付款期限、成品数量与原材料数量、质量补救与更换材料；新增质保与生效等精细要求。
- backend/review_v2/engine.py：优先校验最终quote；接入承揽要求；同步证据位置；发布绑定按要素再次验证直接支持关系，保留原质量门控。
- backend/routers/review_v2.py：将路由和新增证据模块纳入运行代码新鲜度检查。
- backend/tests/test_work_canonical_evidence.py：原合同与正常买卖回归、角色变体、虚假quote反例、逐要素正向支持和全文缺失审计。

## 结果

页面启用大模型重审，后端进程14692，runtime_source_drift=CURRENT。
合同类型work_contract（承揽合同），44项；18通过、25缺失、1不适用。
release_quality_gate=REPORT_READY，failures=[]；没有放宽或关闭质量门控。

- 验收10个工作日：第六条第3项，跨审查要素采用相同源标识。
- 产品质保12个月：第二条第8项，保留为COVERED正向要素。
- 成品数量：第一条5000套；不使用第三条18吨原材料数量。
- 生效日期：独立合同生效日期字段2026年9月8日；不使用技术资料保密义务的生效时间。
- 第三条更换材料限制不支持修理、更换等质量救济。

153项相关回归通过：承揽、买卖、融资租赁共享事实及借款成本组合。逐项审计测试再次通过7项。git diff --check通过。

完整确定性结果：work-fixed.json；逐要素状态、quote和location审计：work-element-audit.json。
