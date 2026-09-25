# 用户风险画像：诊断与回归记录

日期：2026-09-09。按“先检查、先说明诊断、再修改”执行。本次保留工作区已有的大量未提交改动。

## 根因与影响

这不是纯文案问题，而是画像建模缺陷和上下文状态污染共同造成。

1. `frontend/src/views/ContractReviewV2.vue` 原来把身份初始化为“个人租客/买方”，场景初始化为“居住用途”。身份选项混入企业规模；除技术合同外，所有类型使用同一身份列表。除买卖合同外，所有类型使用租赁场景列表。快捷预设重写租赁身份和场景，类型 watcher 只处理买卖、技术与租赁的少量转换。重新识别的结果未回填输入画像，旧请求没有防止覆盖新状态的版本检查。
2. `backend/review_v2/user_profile.py` 的 dataclass、default、from_dict 缺字段默认值均为租赁画像。`engine.py::_request_scoped_profile` 仅处理买卖场景；域识别后的其他类型没有完整校验画像归属。
3. `perspective_resolution.py` 没有承揽、运输等专用角色兼容关系。历史 `.runtime-logs/work-fixed.json` 的 `contract_type=work_contract`，但 `profile.user_identity` 和 `perspective_resolution.requested_role` 为“个人租客/买方”；BUYER、LESSEE 被拒绝后角色变为 OTHER，证明污染进入了实际审查参数。
4. 三个附加分析接口在引擎处理后继续使用原始 profile，而不是引擎返回的有效 profile。

| 字段 | 实际用途及影响边界 |
|---|---|
| user_identity / review_role | 用户身份与审查立场，进入 perspective_resolution、contract_context、逐项 decision_trace；错误身份会造成错误默认立场或降为中性立场。 |
| contract_scenario | 场景和返回画像。旧版后续还会被 report_context 的场景标签覆盖，造成 UI 与响应不一致。 |
| risk_appetite | 实际参与风险后处理；激进模式仍会降低中风险等级。本次保留既有通用偏好规则。 |
| bargaining_position | 实际进入逐项审查轨迹、谈判、诉讼成本收益与地域分析。 |
| 租赁优先审查点映射 | 存在于画像模块；当前主审查流程只导入相关函数，没有实际调用，不能宣称这些映射已将非租赁规则替换成租赁规则。已补类型门禁防止其他调用方误用。 |
| LLM prompt / 清单选择 | 当前 LLM 条款复核 prompt 读取清单、候选合同条款及规则初判，不直接接收画像。清单由合同类型/文本分类选择，未发现由租客身份选择租赁清单。 |

因此此前确有实际参数污染及立场退化；不能认定只是展示错误，也不能认定所有历史审查结论错误。未执行付费云模型前后对照；本次回归使用真实本地规则引擎。

## 存储、缓存及检索范围

全局检索覆盖源代码、配置、清单模板、测试、脚本、历史日志与 artifacts 快照；当前实现集中在上述模块。押金裁判模块及房屋租赁清单中的租客、居住用途属于专用场景，保留。

当前 V2 页面没有画像 localStorage/sessionStorage 写入；文件审查接口没有规则/证据/报告结果缓存。历史日志及快照含污染值，但当前入口不读取这些快照初始化画像。

检查了本地 SQLite 文件结构，没有专用画像表、画像字段或租赁默认值映射。根目录 app.db 的 record.report_markdown、record.metadata_json、task_record.metadata_json、task_record.result 未命中“个人租客/居住用途”。backend/app.db 的历史记录扫描被 SQLite `database disk image is malformed` 阻断，不能确认该库全部历史记录。未修改数据库或历史报告。

## 修改文件及逻辑

| 文件 | 修改 |
|---|---|
| `backend/review_v2/profile_catalog.py`（新增） | 按类型提供角色、场景及旧角色别名；未知类型中性回退。身份不再混用企业规模或风险偏好。 |
| `backend/review_v2/user_profile.py` | 中性未绑定默认值；增加 contract_type 归属；识别后复制并校验画像，保留通用偏好；清理旧租赁身份/场景及跨类型状态。保留合法专用工厂，投资者工厂限定投资类型；租赁优先点增加类型门禁，去掉企业规模与审查点的混用映射。 |
| `backend/review_v2/engine.py` | 在最终类型识别后归一化；有效身份与解析后的角色一致；补齐承揽、运输、投资、劳动等对方角色；通用报告场景标签不再抹掉用户的有效专用场景。 |
| `backend/review_v2/perspective_resolution.py` | 补齐承揽、运输等合同角色，以及融资方；允许显式中性立场通过兼容校验；保留现有技术子类型角色解析。 |
| `backend/routers/review_v2.py` | 新增带认证的 GET /review-v2/profile-options；三个附加分析接口使用引擎返回画像。 |
| `frontend/src/utils/api.js` | 请求后端画像配置。 |
| `frontend/src/utils/reviewProfile.mjs`（新增） | 管理独立通用偏好和合同上下文；类型变化、换文件清理上下文；类型重新识别同步身份、场景；预设只调整通用偏好，标签跟随当前角色。 |
| `frontend/src/views/ContractReviewV2.vue` | 使用配置和状态模块；构造包含合同归属与 review_role 的参数；请求期间配置改变后拒绝旧响应；回填有效类型、身份、场景。 |
| `backend/tests/test_contract_scoped_user_profile.py`（新增） | 画像归一化、六类真实引擎及 DOCX HTTP 入口、识别转换、角色别名、附加分析一致性回归。 |
| `frontend/src/utils/reviewProfile.test.mjs`（新增） | 使用真实后端配置测试 Vue 状态切换、预设、有效参数一致性。 |
| `frontend/src/utils/reviewProfilePage.test.mjs`（新增） | 编译并挂载真实 SFC setup，模拟网络验证回填以及旧响应覆盖保护；不是浏览器像素测试。 |
| `artifacts/profile_scope/baseline_probe.py`（新增） | 仅在内存撤回本次核心画像改动，保留既有工作区改动，用于复现历史回归失败。 |

## 验收场景

| 合同类型 | 身份选项 | 结果 |
|---|---|---|
| 租赁 | 承租人 / 出租人 | 保留居住用途；预设不会改变已选择的出租人立场。 |
| 承揽 | 定作方 / 承揽方 | 无个人租客、居住用途、投资/转租残留；WORK_CUSTOMER / WORK_CONTRACTOR。 |
| 运输 | 托运人 / 承运人 / 收货人 | 无租赁画像残留；CONSIGNOR / CARRIER / CONSIGNEE。 |
| 投资 | 投资方 / 融资方 | 无租赁画像残留；INVESTOR / TARGET_COMPANY。 |
| 股东协议 | 股东 / 公司 | 无租赁画像残留；保留股权治理场景。 |
| 劳动 | 劳动者 / 用人单位 | 无租赁画像残留；WORKER / LABOR_EMPLOYER。 |

还覆盖买卖的买方/卖方、股权转让的转让方/受让方、未知类型的合同当事人。六类均通过真实规则引擎与 DOCX HTTP 接口，校验返回 profile、perspective_resolution、contract_context；前端另验证 buildProfile 与显示值一致。类型切换、同类型换文件、重新识别和晚返回响应都有测试。

## 回归中的既有失败

最终确认集：后端 **164 passed**（本次新增画像测试 98 项，加现有买卖、运输、承揽、公司设立、立场冻结测试 66 项），前端 **16 passed**；`npm run build` 成功，`git diff --check` 无空白错误。

可复现命令（仓库根目录 PowerShell）：

```powershell
$env:PYTHONPATH='backend;backend/tests'
$env:PYTHONIOENCODING='utf-8'
python -m pytest backend/tests/test_contract_scoped_user_profile.py backend/tests/test_sale_review_checklist.py backend/tests/test_transportation_review_checklist.py backend/tests/test_work_contract_review_checklist.py backend/tests/test_company_formation_routing.py backend/tests/test_quality6_7_final_freeze.py -q --disable-warnings --tb=short
```

前端目录执行：

```powershell
node --test src/utils/reviewProfile.test.mjs src/utils/reviewProfilePage.test.mjs
npm run build
```

扩大回归中以下六项失败，均在 baseline_probe 的本次改动撤回对照中复现相同失败：

1. `test_review_v2_house_lease.py::test_quality_phase_two_separates_coverage_risk_priority_and_findings`：旧测试要求 BLOCKED，当前原有实现返回 REPORT_READY。
2. `test_priority_contract_review.py::test_each_type_end_to_end[normal-operating_cooperation]`：原夹具缺少 operating_cooperation，KeyError。
3. 同文件 `[normal-non_compete]`：原测试要求通过，实际部分覆盖。
4. 同文件 `[normal-equity_pledge]`：原测试要求通过，实际部分覆盖。
5. `test_technical_service_dynamic_roles_and_grounding.py::test_service_acceptance_and_new_result_core_facts_are_not_keyword_passes`：原测试要求部分覆盖，实际缺失。
6. 同文件 `test_third_party_claim_direction_changes_between_provider_and_recipient`：原测试要求部分覆盖，实际风险条款。

这些失败未通过更改预期或审查规则掩盖。完整仓库回归未全量执行；已执行的扩大回归不能宣称全绿。前端生产构建通过，存在原有 Vite CJS/依赖注释/大包警告。

## 生效范围

本次完成工作区源码修复及前端构建，没有重启或部署正在运行的服务。后端重新加载代码、前端更新后生效。历史污染报告不会自动重写，需要重新审查才能生成新的有效画像与立场。
