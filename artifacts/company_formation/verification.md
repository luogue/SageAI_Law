# 入股合作协议：分类、路由与适用性修复验收

## 最终结果

- 原文件：`F:/ai/Sage/test_data/83 投资协议.docx`，未修改或裁剪；正文标题为“入股合作协议书”。
- 文件 SHA256：`8bdcbca80dba56ef998d4511d939bbca4ce4bf514895117042f33a1e3e502f12`。
- 全文抽取 3924 字；规范化全文 SHA256：`64c9da2ab188f47cb00625c2b9142d3bbad20e5fb9bc04084e36c4bb824311f8`。
- 分类、条款解析、规则审查、缺失审计使用同一份全文，哈希一致。
- `contract_type=shareholders`；`contract_family=EQUITY_INVESTMENT`。
- `scenario=股东合作协议`；`role=equity_party / 股权协议当事人`。
- `release_quality_gate=REPORT_READY`，无阻断项。
- 共17项：14项公司设立专项，3项通用事项；买卖专项加载数0。
- 出资期限要素识别为已覆盖，没有输出“交货时间”。
- 两条试用买卖规则在独立适用性审计中均为不适用；即使强制仅检查买卖触发条件，也不能被“测试用途”触发。

## 根因及修复

1. 原分类仅支持“股东协议/股东合作协议”等标题，漏掉“入股合作协议书”及设立公司的主交易事实。在标题未匹配后，设备/材料和经营范围中的“销售”两组词各得4分，SALE=8被误认为高置信度，并覆盖用户选择的investment。新增可追溯的共同设立目的与注册资本、出资、股权、治理、盈亏组合证据，排除经营范围作为买卖履约证据；已识别的股权主交易不再被通用词频二次覆盖。
2. 不存在OTHER映射成SALE的根因：注册表对不支持类型抛出异常，空类型原默认是租赁；本轮问题是错误的高置信度DOCUMENT_OVERRIDE。低置信度仍保留明确用户选择，不新增SALE默认值。
3. “测试用途”包含连续字符“试用”，原子串门禁误判为试用交易。增加正文触发视图和词边界/否定过滤，并使触发证据审计使用相同逻辑；保留完整原文及原文定位。
4. 股权关系禁止使用货物买卖专项前提；运输专项也必须有运输事实。所有权保留不因分期付款自动触发，路货不因普通运输触发，样品展示不因“样品”一词自动触发。货物质保、验收规则继续属于货物买卖清单，不从出资交付推导。
5. 后处理和规则隔离门禁原来重新调用基础清单，丢失细分场景。本次沿用解析后的清单，保持分类、执行、门禁一致，并验证注入买卖规则会被阻断。
6. 修复适用性三值状态：事实待核验为CONDITIONAL_UNRESOLVED，不得等同CONDITIONAL_NOT_TRIGGERED；明确不适用不能被后续覆盖判定改回缺失。收窄劳动解除专项到其实际节点，避免误拦截租赁解除规则。
7. 报告和页面统一使用解析角色。框架买卖的三项顺位审计补齐客观检索目标，待核验期限的原文保留在证据定位，不再拼入理由造成重复且未登记的事实；租赁适用说明移除内部字段名。

## 本轮修改文件

| 文件 | 作用 |
|---|---|
| `backend/review_v2/transaction_scope.py`（新增） | 主交易目的、经营范围隔离、触发文本与词边界 |
| `backend/review_v2/priority_contract_types.py` | 入股/公司设立识别和股东合作别名 |
| `backend/review_v2/domain_selection.py` | 主股权关系优先、排除经营范围误评分、场景清单校验 |
| `backend/review_v2/domain_resolution.py` | 公司设立事实进入域解析 |
| `backend/review_v2/contract_registry.py` | 公司设立专项清单路由 |
| `backend/review_v2/company_formation_checklist.py`（新增） | 14项设立/股东合作专项及通用审查 |
| `backend/review_v2/engine.py` | 适用性前置、三值状态、后处理清单传递、输出一致性 |
| `backend/review_v2/priority_contract_review.py` | 劳动解除专属规则按实际节点隔离 |
| `backend/routers/review_v2.py` | 新模块纳入生产源码漂移检测 |
| `frontend/src/views/ContractReviewV2.vue` | 立场标签读取已解析角色 |
| `backend/tests/test_company_formation_routing.py`（新增） | 32个参数化及生产入口回归用例 |
| `backend/tests/test_sale_review_checklist.py` | 旧测试改用现有公开状态“待核验” |
| `backend/tests/test_sale_package_evidence.py` | 公开状态断言、已存在通用违约金基数规则的统计断言 |
| `scripts/run_company_formation_acceptance.py`（新增） | 原文完整上传复测、模型配置、哈希及门禁留证 |

未使用姓名、地区、账户、金额或当前合同的固定段落作为生产规则分支。

## 投资审查方向

已覆盖股东/公司身份、资本、认缴实缴、出资方式比例期限违约、非货币及技术出资的适格性/权属/估值/移转、临时账户隔离及资金安全、董事经理监事与股东会表决、控制权僵局、增资与第三方加入、利润亏损及资金留存、优先购买/股权转让、退出与资本维持、章程衔接、生效送达及争议解决。

同文命中的四类直接风险为：客户资源/管理经验作价适格性，单方最终决定，返还原投资，转让违约与效力混同。已有估值金额和再次协商条款分别作为正向证据保留，未整体误判缺失。规则范围为公司设立的基础审查，不宣称穷尽全部投资交易类型。

新增规则依据核对：[全国人大《公司法》](https://www.npc.gov.cn/npc/c2/c30834/202312/t20231229_433999.html)、[市场监管总局《市场主体登记管理条例》](https://www.samr.gov.cn/djzcj/zyfb/zjfb/art/2023/art_2a71fe3f890947e4860918946cb60386.html)。

## 测试结果

- 主链路回归：**145 passed**。包含新增32例、原买卖清单、设备采购完整DOCX生产上传、买卖证据、域冲突、主目的分类、增资/股权证据及注册表。
- 股权类型补充回归：**28 passed**（investment/shareholders/capital_increase/equity_transfer，正常/缺失/风险等场景）。
- 合计本轮相关回归：**173 passed**。
- 前端：`npm run build`通过；保留已有打包体积及第三方注释警告。
- 全文生产接口：FastAPI multipart `/review-v2/file`，真实提取器、路由和响应模型，隔离测试认证；`use_llm=true`，模型Qwen可用且执行，最终REPORT_READY。
- 另外在当前浏览器保留的原文件上实际点击“开始审查”，核对页面类型、立场、3924字、17项以及服务日志。
- 最终浏览器生产请求：`CR-20260909-065336-0B1AA4`，进程11456，`runtime=CURRENT`，`REPORT_READY`且failures为空。见`live-verification.json`及`.runtime-logs/formation-verified.err.log`。
- 不宣称全仓库零失败：首次扩大范围发现8项失败，移除本轮相关生产改动的隔离基线仍复现8项；其中买卖公开状态旧断言已修正，其余7项在竞业、质押和旧规则注册断言范围，未计入上述相关回归通过数。

证据：`final-tests.log`、`equity-regression.log`、`frontend-build.log`、`baseline-failures.log`；最终原文HTTP报告为`final_http/result.json`、`final_http/summary.json`、`final_http/report.md`、`final_http/normalized_input.txt`。

临时基线副本位于`baseline/`；清理被自动审批策略拒绝（blocked by policy），因此保留。
