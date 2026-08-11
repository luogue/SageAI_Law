<template>
  <div class="review-v2-page">
    <section class="review-shell">
      <aside class="control-panel">
        <div class="panel-header">
          <div>
            <p class="eyebrow">审查第二版</p>
            <h1>合同审查引擎</h1>
          </div>
          <el-tag effect="plain" type="success">独立模块</el-tag>
        </div>

        <el-form label-position="top" class="review-form">
          <el-form-item label="合同类型">
            <el-select v-model="contractType" class="full-width">
              <el-option
                v-for="option in contractTypeOptions"
                :key="option.value"
                :label="option.label"
                :value="option.value"
                :disabled="option.disabled"
              />
            </el-select>
          </el-form-item>

          <el-form-item label="报告范围">
            <el-switch
              v-model="includeLowRisk"
              active-text="包含已覆盖/低风险项"
              inactive-text="仅看中高风险"
            />
          </el-form-item>

          <el-form-item label="语义判定">
            <el-switch
              v-model="useLlmReview"
              :disabled="llmStatusLoaded && !llmStatus?.available"
              active-text="启用大模型复核"
              inactive-text="仅用合同原文审查"
            />
            <div
              v-if="llmStatusLoaded"
              class="llm-status"
              :class="{ available: llmStatus?.available, unavailable: !llmStatus?.available }"
            >
              {{ llmStatus.message }}
              <span v-if="llmStatus?.configured_models?.length">
                模型：{{ llmStatus.configured_models.join(' / ') }}
              </span>
            </div>
          </el-form-item>
        </el-form>

        <!-- 用户风险画像 -->
        <div class="profile-panel">
          <div class="profile-header" @click="profileExpanded = !profileExpanded">
            <span class="profile-title">用户风险画像</span>
            <el-icon :class="{ rotated: profileExpanded }"><ArrowDown /></el-icon>
          </div>
          <el-collapse-transition>
            <div v-show="profileExpanded" class="profile-body">
              <div class="preset-row">
                <el-button size="small" @click="setProfilePreset('conservative_individual')">个人租客-保守</el-button>
                <el-button size="small" @click="setProfilePreset('standard')">标准</el-button>
                <el-button size="small" @click="setProfilePreset('aggressive_investor')">投资者-激进</el-button>
              </div>

              <el-form label-position="top" size="small" class="profile-form">
                <el-form-item label="用户身份">
                  <el-select v-model="userIdentity" class="full-width">
                    <el-option v-for="opt in identityOptions" :key="opt" :label="opt" :value="opt" />
                  </el-select>
                </el-form-item>
                <el-form-item label="合同场景">
                  <el-select v-model="contractScenario" class="full-width">
                    <el-option v-for="opt in scenarioOptions" :key="opt" :label="opt" :value="opt" />
                  </el-select>
                </el-form-item>
                <el-form-item label="风险偏好">
                  <el-radio-group v-model="riskAppetite" class="full-width">
                    <el-radio-button v-for="opt in appetiteOptions" :key="opt" :value="opt">{{ opt }}</el-radio-button>
                  </el-radio-group>
                </el-form-item>
                <el-form-item label="交易地位">
                  <el-radio-group v-model="bargainingPosition" class="full-width">
                    <el-radio-button v-for="opt in positionOptions" :key="opt" :value="opt">{{ opt }}</el-radio-button>
                  </el-radio-group>
                </el-form-item>
                <el-form-item label="案件管辖地">
                  <el-select v-model="jurisdiction" class="full-width">
                    <el-option v-for="opt in jurisdictionOptions" :key="opt" :label="opt" :value="opt" />
                  </el-select>
                </el-form-item>
              </el-form>
            </div>
          </el-collapse-transition>
        </div>

        <div
          class="upload-zone"
          :class="{ dragging: isDragging, selected: selectedFile }"
          @dragover.prevent="isDragging = true"
          @dragleave.prevent="isDragging = false"
          @drop.prevent="handleDrop"
          @click="fileInput?.click()"
        >
          <input
            ref="fileInput"
            type="file"
            accept=".doc,.docx,.pdf"
            hidden
            @change="handleFileChange"
          />
          <el-icon class="upload-icon"><UploadFilled /></el-icon>
          <div class="upload-title">{{ selectedFile ? selectedFile.name : '上传合同文件' }}</div>
          <div class="upload-hint">支持 .doc / .docx / .pdf，系统按审查清单逐项检查</div>
        </div>

        <div class="action-row">
          <el-button :icon="RefreshLeft" @click="resetAll">清空</el-button>
          <el-button type="primary" :icon="Search" :loading="loading" @click="runReview">
            {{ loading ? '审查中' : '开始审查' }}
          </el-button>
        </div>

        <el-steps :active="stepActive" finish-status="success" direction="vertical" class="progress-steps">
          <el-step title="上传合同" description="读取 Word 或 PDF 文本" />
          <el-step title="加载清单" description="按合同类型加载对应审查清单" />
          <el-step title="生成报告" description="输出风险提示和修改建议" />
        </el-steps>
      </aside>

      <main class="report-panel">
        <template v-if="report">
          <div class="report-toolbar">
            <div>
              <div class="view-mode-switch">
                <el-radio-group v-model="reportViewMode" size="small">
                  <el-radio-button value="checklist">审查清单</el-radio-button>
                  <el-radio-button value="litigation">诉讼分析</el-radio-button>
                  <el-radio-button value="negotiation">商业谈判</el-radio-button>
                  <el-radio-button value="jurisdiction">地域预判</el-radio-button>
                </el-radio-group>
              </div>
              <p class="eyebrow">结构化报告</p>
              <h2>{{ report.contract_type_name }}</h2>
              <p class="file-meta">{{ report.filename }} · 已抽取 {{ report.extracted_text_length }} 字</p>
            </div>
            <div class="toolbar-actions" v-if="reportViewMode === 'checklist'">
              <el-radio-group v-model="riskFilter" size="small">
                <el-radio-button
                  v-for="option in riskFilterOptions"
                  :key="option"
                  :label="option"
                  :value="option"
                >
                  {{ priorityFilterLabel(option) }}
                </el-radio-button>
              </el-radio-group>
              <el-select v-model="coverageFilter" class="coverage-filter" size="small">
                <el-option
                  v-for="option in coverageFilterOptions"
                  :key="option"
                  :label="option === '全部' ? '全部覆盖状态' : option"
                  :value="option"
                />
              </el-select>
              <el-select v-model="issueTypeFilter" class="issue-filter" size="small">
                <el-option
                  v-for="option in issueTypeFilterOptions"
                  :key="option"
                  :label="option === '全部' ? '全部问题类型' : option"
                  :value="option"
                />
              </el-select>
              <el-select v-model="judgeSourceFilter" class="source-filter" size="small">
                <el-option
                  v-for="option in judgeSourceFilterOptions"
                  :key="option.value"
                  :label="option.label"
                  :value="option.value"
                />
              </el-select>
              <el-button
                type="primary"
                plain
                :icon="Download"
                :loading="exportingType === 'pdf'"
                :disabled="!!exportingType"
                @click="downloadReport('pdf')"
              >
                导出 PDF
              </el-button>
              <el-button
                type="success"
                plain
                :icon="Download"
                :loading="exportingType === 'docx'"
                :disabled="!!exportingType"
                @click="downloadReport('docx')"
              >
                导出 Word
              </el-button>
            </div>
          </div>

          <!-- ====== 审查清单视图 ====== -->
          <template v-if="reportViewMode === 'checklist'">
          <!-- 用户画像摘要 -->
          <div v-if="report.profile" class="profile-summary">
            <div class="profile-summary-header">
              <el-icon><User /></el-icon>
              <span>用户画像</span>
            </div>
            <div class="profile-summary-tags">
              <el-tag size="small" type="info">{{ report.profile.user_identity }}</el-tag>
              <el-tag size="small" type="info">{{ report.profile.contract_scenario }}</el-tag>
              <el-tag size="small" :type="report.profile.risk_appetite === '保守' ? 'danger' : report.profile.risk_appetite === '激进' ? 'success' : 'warning'">
                {{ report.profile.risk_appetite }}
              </el-tag>
              <el-tag size="small" :type="report.profile.bargaining_position === '弱势方' ? 'warning' : report.profile.bargaining_position === '强势方' ? 'success' : 'info'">
                {{ report.profile.bargaining_position }}
              </el-tag>
            </div>
          </div>

          <div class="format-notice">
            {{ report.report_notice || '本报告基于完整合同模板逐项审查，部分缺失项可能因合同格式简略所致，建议结合合同实际用途判断优先级。' }}
          </div>

          <div class="summary-grid">
            <!-- 分级行动建议 -->
            <div class="summary-card must">
              <span>必须修改</span>
              <strong>{{ report.risk_finding_summary?.重大风险 || actionStats.must }}</strong>
            </div>
            <div class="summary-card suggest">
              <span>建议修改</span>
              <strong>{{ report.risk_finding_summary?.中等风险 || actionStats.suggest }}</strong>
            </div>
            <div class="summary-card consider">
              <span>可考虑改</span>
              <strong>{{ report.risk_finding_summary?.低风险 || actionStats.consider }}</strong>
            </div>
            <div class="summary-card high">
              <span>已覆盖</span>
              <strong>{{ report.coverage_summary?.通过 || 0 }}</strong>
            </div>
            <div class="summary-card medium">
              <span>部分覆盖</span>
              <strong>{{ report.coverage_summary?.部分覆盖 || 0 }}</strong>
            </div>
            <div class="summary-card low">
              <span>缺失</span>
              <strong>{{ report.coverage_summary?.缺失 || 0 }}</strong>
            </div>
            <div class="summary-card na">
              <span>不适用</span>
              <strong>{{ report.coverage_summary?.不适用 || 0 }}</strong>
            </div>
            <div class="summary-card total">
              <span>审查项</span>
              <strong>{{ report.all_items_count }}</strong>
            </div>
          </div>

          <div v-if="report.global_fallback_reason" class="global-fallback">
            {{ report.global_fallback_reason }}
          </div>

          <section class="core-risk-panel">
            <div class="section-title">核心风险摘要</div>
            <div v-if="coreRiskItems.length" class="core-risk-list">
              <div v-for="item in coreRiskItems" :key="item.finding_id || item.item_id" class="core-risk-row">
                <el-tag :type="riskTagType(item.severity || item.risk_level)" effect="dark">{{ riskLabel(item.severity || item.risk_level) }}</el-tag>
                <div>
                  <strong>{{ item.title }}</strong>
                  <p>{{ userFacingText(item.recommendation || item.risk_point_description) }}</p>
                </div>
              </div>
            </div>
            <div v-else class="empty-core-risk">未发现需要优先处理的高风险或重大经济后果事项。</div>
          </section>

          <div class="review-list">
            <article v-for="item in filteredItems" :key="item.item_id" class="review-item">
              <header class="item-header">
                <div>
                  <div class="item-title">{{ item.item_id }} · {{ item.title }}</div>
                  <div class="item-status">
                    {{ item.status }} · {{ item.coverage_status }} · {{ item.issue_type || '未分类' }} · {{ judgeSourceLabel(item.judge_source) }}
                  </div>
                </div>
                <el-tag :type="coverageTagType(item.coverage_status)" effect="dark">{{ item.coverage_status }}</el-tag>
              </header>

              <dl class="item-body">
                <dt>证据来源</dt>
                <dd>
                  {{ judgeSourceLabel(item.judge_source) }}
                  <span v-if="item.llm_confidence"> · 置信度 {{ confidenceLabel(item.llm_confidence) }}</span>
                </dd>
                <dt>系统判断</dt>
                <dd>{{ userFacingText(item.reasoning_summary) }}</dd>
                <dt>问题类型</dt>
                <dd>{{ item.issue_type || '未分类' }}</dd>
                <dt>原文位置</dt>
                <dd>{{ item.evidence_location || '未召回正式条款' }}</dd>
                <dt>命中原文</dt>
                <dd>
                  <div v-if="item.evidence_clauses?.length" class="evidence-list">
                    <details
                      v-for="evidence in item.evidence_clauses"
                      :key="evidence.clause_id"
                      class="evidence-item"
                    >
                      <summary>{{ evidence.location }} · {{ evidence.section_type }}</summary>
                      <p>{{ evidence.text }}</p>
                    </details>
                  </div>
                  <span v-else class="no-evidence">无正式条款证据</span>
                </dd>
                <dt>【风险点描述】</dt>
                <dd>{{ userFacingText(item.risk_point_description) }}</dd>
                <dt>【{{ legalConsequenceLabel(item) }}】</dt>
                <dd>{{ userFacingText(legalConsequenceText(item)) }}</dd>
                <template v-if="suggestedClauseLabel(item)">
                  <dt>【{{ suggestedClauseLabel(item) }}】</dt>
                  <dd>{{ item.suggested_clause_example }}</dd>
                </template>
                <dt>【法律依据】</dt>
                <dd>{{ item.legal_basis_index }}</dd>
                <template v-if="item.reasoning">
                  <dt>【推理过程】</dt>
                  <dd>
                    <pre class="reasoning-chain">{{ item.reasoning }}</pre>
                  </dd>
                </template>
                <template v-if="item.citation && Object.keys(item.citation).length">
                  <dt>【证据定位】</dt>
                  <dd>
                    <ul class="citation-list">
                      <li><strong>条款编号：</strong>{{ item.citation.clause_number || '未召回正式条款' }}</li>
                      <li><strong>原文片段：</strong>{{ item.citation.original_excerpt || '无正式条款证据' }}</li>
                      <li><strong>位置描述：</strong>{{ item.citation.position_description || '合同正式条款及附件中未定位到可验证条款' }}</li>
                    </ul>
                  </dd>
                </template>
              </dl>

              <div class="review-controls">
                <el-radio-group v-model="item.review_status" size="small">
                  <el-radio-button label="待处理" />
                  <el-radio-button label="已处理" />
                  <el-radio-button label="忽略" />
                </el-radio-group>
                <el-input
                  v-model="item.reviewer_note"
                  class="note-input"
                  size="small"
                  clearable
                  placeholder="律师复核备注"
                />
              </div>
            </article>
          </div>
          </template>

          <!-- ====== 诉讼分析视图 ====== -->
          <template v-if="reportViewMode === 'litigation'">
            <div v-if="report.litigation?.disclaimer" class="litigation-disclaimer">
              <el-icon><WarningFilled /></el-icon>
              <span>{{ report.litigation.disclaimer }}</span>
            </div>

            <div v-if="report.litigation?.summary" class="summary-grid">
              <div class="summary-card must">
                <span>建议起诉</span>
                <strong>{{ report.litigation.summary['建议起诉'] || 0 }}</strong>
              </div>
              <div class="summary-card suggest">
                <span>建议协商</span>
                <strong>{{ report.litigation.summary['建议协商'] || 0 }}</strong>
              </div>
              <div class="summary-card consider">
                <span>不建议起诉</span>
                <strong>{{ report.litigation.summary['不建议起诉'] || 0 }}</strong>
              </div>
            </div>

            <div class="review-list">
              <article v-for="item in (report.litigation?.items || [])" :key="item.item_id" class="review-item litigation-item">
                <header class="item-header">
                  <div>
                    <div class="item-title">{{ item.item_id }} · {{ item.title }}</div>
                    <div class="item-status">审查重要度：{{ importanceLabel(item.review_importance) }} · 行动优先级：{{ priorityLabel(item.action_priority || item.review_priority) }}</div>
                  </div>
                  <el-tag :type="coverageTagType(item.coverage_status)" effect="dark">{{ item.coverage_status || '未标注' }}</el-tag>
                </header>

                <!-- 证据缺口 -->
                <dl class="item-body">
                  <dt>🔴 缺了几乎必输</dt>
                  <dd>
                    <ul v-if="item.evidence_gaps?.filter(g => g.severity === 'critical').length" class="gap-list">
                      <li v-for="gap in item.evidence_gaps.filter(g => g.severity === 'critical')" :key="gap.evidence_name" class="gap-critical">
                        <strong>{{ gap.evidence_name }}</strong>：{{ gap.description }}
                        <div v-if="gap.source_hint" class="gap-hint">获取方式：{{ gap.source_hint }}</div>
                      </li>
                    </ul>
                    <span v-else class="no-evidence">无关键证据缺口</span>
                  </dd>

                  <dt>🟡 建议补充</dt>
                  <dd>
                    <ul v-if="item.evidence_gaps?.filter(g => g.severity === 'recommended').length" class="gap-list">
                      <li v-for="gap in item.evidence_gaps.filter(g => g.severity === 'recommended')" :key="gap.evidence_name" class="gap-recommended">
                        <strong>{{ gap.evidence_name }}</strong>：{{ gap.description }}
                        <div v-if="gap.source_hint" class="gap-hint">获取方式：{{ gap.source_hint }}</div>
                      </li>
                    </ul>
                    <span v-else class="no-evidence">无建议补充证据</span>
                  </dd>

                  <dt>🟢 证据充分</dt>
                  <dd>
                    <ul v-if="item.evidence_gaps?.filter(g => g.severity === 'sufficient').length" class="gap-list">
                      <li v-for="gap in item.evidence_gaps.filter(g => g.severity === 'sufficient')" :key="gap.evidence_name" class="gap-sufficient">
                        ✅ {{ gap.evidence_name }}：{{ gap.description }}
                      </li>
                    </ul>
                    <span v-else class="no-evidence">需进一步核实证据准备情况</span>
                  </dd>
                </dl>

                <!-- 法院裁量预测 -->
                <dl v-if="item.court_prediction" class="item-body prediction-section">
                  <dt>⚖️ 法院裁量预测</dt>
                  <dd>
                    <div class="prediction-row"><span class="pred-label">合同约定：</span>{{ item.court_prediction.contract_terms }}</div>
                    <div class="prediction-row"><span class="pred-label">法院大概率支持：</span>{{ item.court_prediction.likely_court_view }}</div>
                    <div class="prediction-row"><span class="pred-label">法律依据：</span><code>{{ item.court_prediction.legal_basis }}</code></div>
                    <div v-if="item.court_prediction.amount_range" class="prediction-row">
                      <span class="pred-label">可执行金额范围：</span><strong>{{ item.court_prediction.amount_range }}</strong>
                    </div>
                    <div v-if="item.court_prediction.reference_cases" class="prediction-row">
                      <span class="pred-label">参考判例：</span>{{ item.court_prediction.reference_cases }}
                    </div>
                  </dd>
                </dl>

                <!-- 成本收益 -->
                <dl v-if="item.cost_benefit" class="item-body cost-section">
                  <dt>💰 成本收益评估</dt>
                  <dd>
                    <div class="cost-grid">
                      <div class="cost-item">
                        <span class="cost-label">争议金额</span>
                        <strong>{{ item.cost_benefit.dispute_amount?.toLocaleString() }} 元</strong>
                      </div>
                      <div class="cost-item">
                        <span class="cost-label">预估诉讼费</span>
                        <strong>{{ item.cost_benefit.litigation_fee?.toLocaleString() }} 元</strong>
                      </div>
                      <div class="cost-item">
                        <span class="cost-label">时间成本</span>
                        <span>{{ item.cost_benefit.time_cost }}</span>
                      </div>
                      <div class="cost-item">
                        <span class="cost-label">执行风险</span>
                        <span>{{ item.cost_benefit.enforcement_risk }}</span>
                      </div>
                    </div>
                    <div class="recommendation-badge" :class="item.cost_benefit.recommendation">
                      <strong>{{ item.cost_benefit.recommendation }}</strong>
                      <p>{{ item.cost_benefit.recommendation_reason }}</p>
                    </div>
                  </dd>
                </dl>
              </article>
            </div>

            <el-empty v-if="!report.litigation?.items?.length" description="当前审查结果中无高/中风险条款，无需诉讼分析" />
          </template>

          <!-- ====== 商业谈判视图 ====== -->
          <template v-if="reportViewMode === 'negotiation'">
            <div v-if="report.negotiation?.disclaimer" class="litigation-disclaimer">
              <el-icon><WarningFilled /></el-icon>
              <span>{{ report.negotiation.disclaimer }}</span>
            </div>

            <!-- 整体策略 -->
            <div v-if="report.negotiation?.overall_strategy" class="negotiation-strategy">
              <div class="strategy-content" v-html="formatStrategy(report.negotiation.overall_strategy)"></div>
            </div>

            <!-- 分类清单 -->
            <div v-if="report.negotiation" class="summary-grid">
              <div class="summary-card must">
                <span>必争项</span>
                <strong>{{ report.negotiation.must_fight?.length || 0 }}</strong>
              </div>
              <div class="summary-card suggest">
                <span>核心项</span>
                <strong>{{ report.negotiation.core_negotiate?.length || 0 }}</strong>
              </div>
              <div class="summary-card consider">
                <span>灵活项</span>
                <strong>{{ report.negotiation.flexible?.length || 0 }}</strong>
              </div>
            </div>

            <div class="review-list">
              <article v-for="item in (report.negotiation?.items || [])" :key="item.item_id" class="review-item negotiation-item">
                <header class="item-header">
                  <div>
                    <div class="item-title">{{ item.item_id }} · {{ item.title }}</div>
                    <div class="item-status">审查重要度：{{ importanceLabel(item.review_importance) }} · 行动优先级：{{ priorityLabel(item.action_priority || item.review_priority) }}</div>
                  </div>
                  <el-tag :type="negotiationPriorityTag(item.negotiation_priority)" effect="dark">
                    {{ item.negotiation_priority }}
                  </el-tag>
                </header>

                <dl class="item-body">
                  <!-- 对方真实意图 -->
                  <dt>对方真实意图</dt>
                  <dd>
                    <div class="intent-box">
                      <div><strong>可能担心：</strong>{{ item.counterparty_intent?.likely_concern }}</div>
                      <div><strong>希望获得：</strong>{{ item.counterparty_intent?.likely_want }}</div>
                      <div v-if="item.counterparty_intent?.pressure_points"><strong>谈判压力点：</strong>{{ item.counterparty_intent.pressure_points }}</div>
                    </div>
                  </dd>

                  <!-- 替代方案 -->
                  <dt>替代方案</dt>
                  <dd>
                    <div v-for="(alt, ai) in item.alternatives" :key="ai" class="alternative-item">
                      <div class="alt-proposal">{{ alt.proposal }}</div>
                      <div class="alt-meta">
                        <el-tag size="small" type="info">影响：{{ alt.impact }}</el-tag>
                        <el-tag size="small" :type="alt.feasibility === '高' ? 'success' : alt.feasibility === '中' ? 'warning' : 'info'">
                          可行性：{{ alt.feasibility }}
                        </el-tag>
                      </div>
                    </div>
                  </dd>

                  <!-- 交换筹码 -->
                  <dt>交换筹码建议</dt>
                  <dd>
                    <div class="tradeoff-box">
                      <div class="tradeoff-row"><span class="give-label">你可以让步：</span>{{ item.tradeoff?.what_you_give }}</div>
                      <div class="tradeoff-row"><span class="ask-label">要求对方回报：</span>{{ item.tradeoff?.what_you_ask }}</div>
                      <div class="tradeoff-row rationale">{{ item.tradeoff?.rationale }}</div>
                    </div>
                  </dd>

                  <!-- 谈判话术 -->
                  <dt>谈判话术</dt>
                  <dd>
                    <div class="script-box">
                      {{ item.script }}
                    </div>
                  </dd>
                </dl>
              </article>
            </div>

            <el-empty v-if="!report.negotiation?.items?.length" description="当前审查结果中无高/中风险条款，无需谈判分析" />
          </template>

          <!-- ====== 跨地域裁判预判视图 ====== -->
          <template v-if="reportViewMode === 'jurisdiction'">
            <div v-if="report.jurisdiction?.disclaimer" class="litigation-disclaimer">
              <el-icon><WarningFilled /></el-icon>
              <span>{{ report.jurisdiction.disclaimer }}</span>
            </div>

            <!-- 地域信息 -->
            <div v-if="report.jurisdiction" class="jurisdiction-header">
              <el-tag type="primary" size="large">管辖地：{{ report.jurisdiction.jurisdiction || '北京' }}</el-tag>
            </div>

            <!-- 整体环境评估 -->
            <div v-if="report.jurisdiction?.environment_assessment" class="negotiation-strategy">
              <div class="strategy-content" v-html="formatStrategy(report.jurisdiction.environment_assessment)"></div>
            </div>

            <!-- 管辖策略总结 -->
            <div v-if="report.jurisdiction?.jurisdiction_strategy_summary" class="jurisdiction-summary-box">
              <el-icon><InfoFilled /></el-icon>
              <span>{{ report.jurisdiction.jurisdiction_strategy_summary }}</span>
            </div>

            <div class="review-list">
              <article v-for="item in (report.jurisdiction?.items || [])" :key="item.item_id" class="review-item jurisdiction-item">
                <header class="item-header">
                  <div>
                    <div class="item-title">{{ item.item_id }} · {{ item.title }}</div>
                    <div class="item-status">审查重要度：{{ importanceLabel(item.review_importance) }} · 行动优先级：{{ priorityLabel(item.action_priority || item.review_priority) }}</div>
                  </div>
                  <el-tag :type="coverageTagType(item.coverage_status)" effect="dark">{{ item.coverage_status || '未标注' }}</el-tag>
                </header>

                <dl class="item-body">
                  <!-- 本地法院倾向 -->
                  <dt>本地法院倾向</dt>
                  <dd>
                    <div class="tendency-box">
                      {{ item.local_court_tendency }}
                    </div>
                  </dd>

                  <!-- 法律基础 -->
                  <dt>法律基础</dt>
                  <dd>
                    <div class="legal-basis-box">
                      {{ item.legal_basis }}
                    </div>
                  </dd>

                  <!-- 本地判例 -->
                  <dt>本地判例参考</dt>
                  <dd>
                    <div v-for="(caseItem, ci) in item.local_cases" :key="ci" class="case-item">
                      <div class="case-header">{{ caseItem.case_id }}</div>
                      <div class="case-court">{{ caseItem.court }}</div>
                      <div class="case-conclusion">{{ caseItem.conclusion }}</div>
                      <div class="case-relevance">关联性：{{ caseItem.relevance }}</div>
                    </div>
                    <span v-if="!item.local_cases?.length" class="no-evidence">该地区暂无同类判例可查</span>
                  </dd>

                  <!-- 起诉建议 -->
                  <dt>起诉建议</dt>
                  <dd>
                    <div class="recommendation-badge" :class="item.litigation_recommendation">
                      <strong>{{ item.litigation_recommendation }}</strong>
                      <p>{{ item.recommendation_reason }}</p>
                    </div>
                  </dd>

                  <!-- 管辖策略 -->
                  <dt v-if="item.jurisdiction_strategy">管辖策略</dt>
                  <dd v-if="item.jurisdiction_strategy">
                    <div class="jurisdiction-tip-box">
                      {{ item.jurisdiction_strategy }}
                    </div>
                  </dd>

                  <!-- 数据来源说明 -->
                  <dd>
                    <div class="data-source-note">{{ item.data_source_note }}</div>
                  </dd>
                </dl>
              </article>
            </div>

            <el-empty v-if="!report.jurisdiction?.items?.length" description="当前审查结果中无高/中风险条款，无需地域预判" />
          </template>
        </template>

        <el-empty v-else description="上传合同后生成审查报告">
          <template #image>
            <el-icon class="empty-icon"><DocumentChecked /></el-icon>
          </template>
        </el-empty>
      </main>
    </section>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { ElMessage } from 'element-plus'
import { ArrowDown, DocumentChecked, Download, InfoFilled, RefreshLeft, Search, UploadFilled, User, WarningFilled } from '@element-plus/icons-vue'
import { exportReviewV2Docx, exportReviewV2Pdf, getReviewV2LlmStatus, reviewContractV2File } from '../utils/api'

defineOptions({
  name: 'ContractReviewV2'
})

const contractTypeOptions = [
  { label: '房屋租赁合同', value: 'house_lease' },
  { label: '买卖合同', value: 'sale' },
  { label: '赠与合同', value: 'gift' },
  { label: '保管合同', value: 'deposit' },
  { label: '承揽合同', value: 'work_contract' },
  { label: '运输合同', value: 'transportation' },
  { label: '委托合同', value: 'agency' },
  { label: '借款合同', value: 'loan' },
  { label: '服务合同', value: 'service' },
  { label: '保证合同', value: 'guarantee' },
  { label: '融资租赁合同', value: 'finance_lease' },
  { label: '仓储合同', value: 'warehouse' },
  { label: '建设工程合同', value: 'construction' },
  { label: '技术合同', value: 'technology' },
  { label: '行纪合同', value: 'commission_agency' },
  { label: '供用电、水、气、热力合同', value: 'utility_supply' },
  { label: '中介合同', value: 'brokerage' },
  { label: '物业服务合同（待导入清单）', value: 'property_management', disabled: true }
]

const riskFilterOptions = ['全部', 'A_CORE', 'B_PRACTICAL', 'C_OPTIMIZATION', 'NONE', 'NOT_APPLICABLE']
const coverageFilterOptions = ['全部', '通过', '部分覆盖', '缺失', '风险条款', '不适用']
const issueTypeFilterOptions = ['全部', '通过', '模板空白', '条款缺陷', '完全缺失', '风险条款', '不适用']
const judgeSourceFilterOptions = [
  { label: '全部证据来源', value: '全部' },
  { label: '语义复核', value: 'llm' },
  { label: '合同原文/结构化事实', value: 'rule_fallback' },
  { label: '适用条件过滤', value: 'applicability_filter' }
]

const fileInput = ref(null)
const selectedFile = ref(null)
const contractType = ref('house_lease')
const includeLowRisk = ref(true)
const useLlmReview = ref(true)
const llmStatus = ref(null)
const llmStatusLoaded = ref(false)
const isDragging = ref(false)
const loading = ref(false)
const exportingType = ref('')
const report = ref(null)
const riskFilter = ref('全部')
const coverageFilter = ref('全部')
const issueTypeFilter = ref('全部')
const judgeSourceFilter = ref('全部')
const stepActive = ref(0)
const reportViewMode = ref('checklist')  // 'checklist' | 'litigation' | 'negotiation'

// 谈判标签样式
function negotiationPriorityTag(priority) {
  if (priority === '必争项') return 'danger'
  if (priority === '核心项') return 'warning'
  return 'success'
}

// 整体策略 Markdown 转 HTML（简单版）
function formatStrategy(text) {
  if (!text) return ''
  return text
    .replace(/^## (.+)$/gm, '<h3>$1</h3>')
    .replace(/^### (.+)$/gm, '<h4>$1</h4>')
    .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
    .replace(/^- (.+)$/gm, '<li>$1</li>')
    .replace(/(\d+)\. (.+)/g, '<li>$1. $2</li>')
    .replace(/\n\n/g, '</p><p>')
    .replace(/\n/g, '<br/>')
}

// 用户风险画像
const profileExpanded = ref(false)
const userIdentity = ref('个人租客/买方')
const contractScenario = ref('居住用途')
const riskAppetite = ref('标准')
const bargainingPosition = ref('均衡方')
const jurisdiction = ref('北京')

const identityOptions = ['个人租客/买方', '小微企业（≤50人）', '中型企业（50-500人）', '大型企业/投资者']
const scenarioOptions = ['居住用途', '商业经营', '投资/转租']
const appetiteOptions = ['保守', '标准', '激进']
const positionOptions = ['强势方', '均衡方', '弱势方']
const jurisdictionOptions = ['北京', '上海', '广州', '深圳', '杭州', '成都', '武汉', '南京', '重庆', '天津', '西安', '长沙']

function buildProfile() {
  return {
    user_identity: userIdentity.value,
    contract_scenario: contractScenario.value,
    risk_appetite: riskAppetite.value,
    bargaining_position: bargainingPosition.value,
    jurisdiction: jurisdiction.value,
  }
}

// 画像快捷预设
function setProfilePreset(preset) {
  if (preset === 'conservative_individual') {
    userIdentity.value = '个人租客/买方'
    contractScenario.value = '居住用途'
    riskAppetite.value = '保守'
    bargainingPosition.value = '弱势方'
  } else if (preset === 'aggressive_investor') {
    userIdentity.value = '大型企业/投资者'
    contractScenario.value = '投资/转租'
    riskAppetite.value = '激进'
    bargainingPosition.value = '强势方'
  } else if (preset === 'standard') {
    userIdentity.value = '个人租客/买方'
    contractScenario.value = '居住用途'
    riskAppetite.value = '标准'
    bargainingPosition.value = '均衡方'
  }
}

const filteredItems = computed(() => {
  if (!report.value?.items) return []
  return report.value.items.filter(item => {
    const riskMatched = riskFilter.value === '全部' || (item.action_priority || item.review_priority) === riskFilter.value
    const coverageMatched = coverageFilter.value === '全部' || item.coverage_status === coverageFilter.value
    const issueMatched = issueTypeFilter.value === '全部' || item.issue_type === issueTypeFilter.value
    const sourceMatched = judgeSourceFilter.value === '全部' || item.judge_source === judgeSourceFilter.value
    return riskMatched && coverageMatched && issueMatched && sourceMatched
  })
})

const coreRiskItems = computed(() => {
  if (report.value?.risk_findings?.length) {
    return report.value.risk_findings.slice(0, 10)
  }
  if (!report.value?.items) return []
  const items = report.value.items.filter(item =>
    item.risk_level === '高' ||
    item.needs_manual_review ||
    ['high', 'critical'].includes(item.economic_impact) ||
    (item.risk_level === '中' && ['A_CORE', 'B_PRACTICAL', 'A', 'B'].includes(item.action_priority || item.review_priority))
  )
  return items
    .sort((a, b) => {
      const rank = item => item.risk_level === '高' ? 0 : ['high', 'critical'].includes(item.economic_impact) ? 1 : 2
      return rank(a) - rank(b) || String(a.item_id).localeCompare(String(b.item_id))
    })
    .slice(0, 10)
})

// 分级行动统计（必须改/建议改/可考虑改）
const actionStats = computed(() => {
  if (!report.value?.items) return { must: 0, suggest: 0, consider: 0, covered: 0 }
  let must = 0, suggest = 0, consider = 0, covered = 0
  for (const item of report.value.items) {
    const s = item.action_suggestion || item.status || ''
    if (s.includes('无需修改') || item.coverage_status === '通过') covered++
    else if (s.includes('必须') || s.includes('优先修改')) must++
    else if (s.includes('建议') || s.includes('需关注')) suggest++
    else if (item.coverage_status !== '不适用') consider++
  }
  return { must, suggest, consider, covered }
})

function judgeSourceLabel(source) {
  if (source === 'llm') return '语义复核'
  if (source === 'applicability_filter') return '适用条件过滤'
  return '合同原文/结构化事实'
}

function confidenceLabel(confidence) {
  const labels = { high: '高', medium: '中', low: '低' }
  return labels[confidence] || confidence
}

function priorityLabel(priority) {
  const labels = {
    A_CORE: '优先处理',
    B_PRACTICAL: '建议处理',
    C_OPTIMIZATION: '可选优化',
    NONE: '无需处理',
    NOT_APPLICABLE: '不适用',
    'N/A': '不适用'
  }
  return labels[priority] || priority || '未标注'
}

function importanceLabel(importance) {
  const labels = {
    CORE: '核心审查项',
    IMPORTANT: '重要审查项',
    NORMAL: '一般审查项'
  }
  return labels[importance] || '一般审查项'
}

function priorityFilterLabel(priority) {
  return priority === '全部' ? '全部优先级' : priorityLabel(priority)
}

function userFacingText(value) {
  let text = String(value || '')
  const replacements = [
    ['统一事实图谱提取', '根据合同原文可确认'],
    ['统一事实图谱识别', '根据合同原文可识别'],
    ['统一事实图谱显示', '根据合同原文显示'],
    ['统一事实图谱', '合同事实'],
    ['Fact Graph', '合同事实'],
    ['Scenario Engine', '金额测算'],
    ['Final Quality Gate', '最终校验'],
    ['Cross Review Consistency Verifier', '一致性校验'],
    ['rule_fallback', '自动审查'],
    ['LLM', '语义复核'],
    ['建议人工复核', '建议重点核对'],
    ['需要人工复核', '需要重点核对'],
  ]
  for (const [from, to] of replacements) {
    text = text.split(from).join(to)
  }
  return text
}

function legalConsequenceLabel(item) {
  if (item.coverage_status === '不适用') return '适用说明'
  if (item.coverage_status === '通过' && item.related_risks?.length) return '关联风险'
  if (item.coverage_status === '通过') return '残余风险'
  return '缺失的法律后果'
}

function legalConsequenceText(item) {
  if (item.coverage_status === '不适用') {
    return item.applicability?.reason || '本项不适用于当前合同。'
  }
  if (item.coverage_status === '通过') {
    if (item.related_risks?.length) {
      return `关联风险 ${item.related_risks.join('、')}：同一条款或事实仍存在需要处理的经济或法律风险。`
    }
    return '无明显残余风险'
  }
  return item.legal_consequence_if_missing
}

function suggestedClauseLabel(item) {
  if (['不适用', '通过'].includes(item.coverage_status)) return ''
  if (item.coverage_status === '部分覆盖') return '建议补充'
  if (item.coverage_status === '风险条款') return '建议修改原条款'
  return '建议新增'
}

async function loadLlmStatus() {
  try {
    const status = await getReviewV2LlmStatus()
    llmStatus.value = status
    if (!status.available) {
      useLlmReview.value = false
    }
  } catch (error) {
    llmStatus.value = {
      available: false,
      configured_models: [],
      message: '无法读取大模型状态，本次默认仅用合同原文审查。'
    }
    useLlmReview.value = false
  } finally {
    llmStatusLoaded.value = true
  }
}

onMounted(() => {
  loadLlmStatus()
})

function handleFileChange(event) {
  const file = event.target.files?.[0]
  setFile(file)
}

function handleDrop(event) {
  isDragging.value = false
  const file = event.dataTransfer.files?.[0]
  setFile(file)
}

function setFile(file) {
  if (!file) return
  const lowerName = file.name.toLowerCase()
  if (!lowerName.endsWith('.doc') && !lowerName.endsWith('.docx') && !lowerName.endsWith('.pdf')) {
    ElMessage.error('请上传 .doc、.docx 或 .pdf 文件')
    return
  }
  if (file.size > 10 * 1024 * 1024) {
    ElMessage.error('文件不能超过 10MB')
    return
  }
  selectedFile.value = file
  stepActive.value = 1
}

async function runReview() {
  if (!selectedFile.value) {
    ElMessage.warning('请先上传合同文件')
    return
  }

  loading.value = true
  stepActive.value = 2
  try {
    const data = await reviewContractV2File(
      selectedFile.value,
      contractType.value,
      includeLowRisk.value,
      useLlmReview.value,
      buildProfile()
    )
    report.value = {
      ...data,
      filename: data.filename || selectedFile.value.name,
      items: (data.items || []).map(item => ({
        ...item,
        review_status: item.review_status || '待处理',
        reviewer_note: item.reviewer_note || ''
      }))
    }
    stepActive.value = 3
    riskFilter.value = '全部'
    coverageFilter.value = '全部'
    issueTypeFilter.value = '全部'
    judgeSourceFilter.value = '全部'
    ElMessage.success('审查报告已生成')
  } catch (error) {
    stepActive.value = 1
    ElMessage.error(error.message || '审查失败')
  } finally {
    loading.value = false
  }
}

function buildExportPayload() {
  return {
    filename: report.value.filename || '合同审查报告',
    contract_type_name: report.value.contract_type_name,
    result: report.value.result,
    summary: report.value.summary,
    risk_finding_summary: report.value.risk_finding_summary,
    coverage_summary: report.value.coverage_summary,
    issue_type_summary: report.value.issue_type_summary,
    judge_source_summary: report.value.judge_source_summary,
    llm_status: report.value.llm_status,
    global_fallback_reason: report.value.global_fallback_reason,
    report_notice: report.value.report_notice,
    review_results_4_0: report.value.review_results_4_0,
    risk_findings: report.value.risk_findings,
    recommendations: report.value.recommendations,
    contract_context: report.value.contract_context,
    overall_assessment: report.value.overall_assessment,
    benchmark_metrics: report.value.benchmark_metrics,
    release_quality_gate: report.value.release_quality_gate,
    quality4_gate: report.value.quality4_gate,
    architecture_status: report.value.architecture_status,
    system_metadata: report.value.system_metadata,
    items: report.value.items
  }
}

function triggerBrowserDownload(blob, filename) {
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = filename
  a.style.display = 'none'
  document.body.appendChild(a)
  a.click()
  document.body.removeChild(a)
  window.setTimeout(() => URL.revokeObjectURL(url), 1000)
}

async function downloadReport(format) {
  if (!report.value) return
  exportingType.value = format
  try {
    const payload = buildExportPayload()
    const blob = format === 'docx'
      ? await exportReviewV2Docx(payload)
      : await exportReviewV2Pdf(payload)
    const baseName = (report.value.filename || '合同审查报告').replace(/\.[^/.]+$/, '')
    const extension = format === 'docx' ? 'docx' : 'pdf'
    triggerBrowserDownload(blob, `${baseName}_审查第二版报告.${extension}`)
    ElMessage.success(`${format === 'docx' ? 'Word' : 'PDF'}报告已开始下载`)
  } catch (error) {
    ElMessage.error(error.message || '报告导出失败')
  } finally {
    exportingType.value = ''
  }
}

function resetAll() {
  selectedFile.value = null
  report.value = null
  riskFilter.value = '全部'
  coverageFilter.value = '全部'
  issueTypeFilter.value = '全部'
  judgeSourceFilter.value = '全部'
  stepActive.value = 0
  if (fileInput.value) fileInput.value.value = ''
}

function riskTagType(level) {
  if (['不适用', 'NONE', 'none'].includes(level)) return 'info'
  if (['高', 'HIGH', 'CRITICAL'].includes(level)) return 'danger'
  if (['中', 'MEDIUM'].includes(level)) return 'warning'
  return 'success'
}

function coverageTagType(status) {
  if (status === '通过') return 'success'
  if (status === '不适用') return 'info'
  if (status === '部分覆盖') return 'warning'
  return 'danger'
}

function riskLabel(level) {
  const labels = {
    NONE: '无风险',
    LOW: '低风险',
    MEDIUM: '中风险',
    HIGH: '高风险',
    CRITICAL: '重大风险',
    none: '无风险',
  }
  if (labels[level]) return labels[level]
  return level === '不适用' ? '不适用' : `${level}风险`
}
</script>

<style scoped>
.review-v2-page {
  min-height: calc(100vh - 56px);
  background: #f5f7fb;
  padding: 24px;
  box-sizing: border-box;
}

.review-shell {
  display: grid;
  grid-template-columns: 360px minmax(0, 1fr);
  gap: 20px;
  max-width: 1360px;
  width: 100%;
  margin: 0 auto;
}

.control-panel,
.report-panel {
  background: #fff;
  border: 1px solid #e6eaf2;
  border-radius: 8px;
  box-shadow: 0 12px 30px rgba(21, 34, 50, 0.06);
}

.control-panel {
  padding: 22px;
  align-self: start;
}

.report-panel {
  min-height: 720px;
  padding: 24px;
}

.panel-header,
.report-toolbar,
.item-header,
.action-row,
.review-controls {
  display: flex;
  align-items: center;
}

.panel-header,
.report-toolbar,
.item-header {
  justify-content: space-between;
  gap: 16px;
}

.panel-header h1,
.report-toolbar h2 {
  margin: 0;
  color: #182230;
}

.panel-header h1 {
  font-size: 24px;
}

.report-toolbar h2 {
  font-size: 22px;
}

.eyebrow {
  margin: 0 0 4px;
  font-size: 12px;
  color: #64748b;
}

.review-form {
  margin-top: 22px;
}

.full-width {
  width: 100%;
}

.upload-zone {
  margin-top: 10px;
  border: 1px dashed #aab7c9;
  border-radius: 8px;
  padding: 34px 18px;
  text-align: center;
  cursor: pointer;
  transition: all 0.2s ease;
  background: #f8fafc;
}

.upload-zone:hover,
.upload-zone.dragging {
  border-color: #4080ff;
  background: #eef6ff;
}

.upload-zone.selected {
  border-style: solid;
  border-color: #67c23a;
  background: #f3fbf0;
}

.upload-icon {
  font-size: 36px;
  color: #4080ff;
}

.upload-title {
  margin-top: 12px;
  font-weight: 700;
  color: #1f2937;
  word-break: break-all;
}

.upload-hint,
.file-meta,
.item-status {
  color: #64748b;
  font-size: 13px;
}

.action-row {
  justify-content: flex-end;
  margin-top: 18px;
  gap: 10px;
}

.llm-status {
  margin-top: 8px;
  padding: 8px 10px;
  border-radius: 8px;
  font-size: 12px;
  line-height: 1.6;
}

.llm-status span {
  display: block;
  margin-top: 2px;
}

.llm-status.available {
  color: #166534;
  background: #f0fdf4;
  border: 1px solid #bbf7d0;
}

.llm-status.unavailable {
  color: #92400e;
  background: #fffbeb;
  border: 1px solid #fde68a;
}

.progress-steps {
  margin-top: 28px;
}

.toolbar-actions {
  display: flex;
  align-items: center;
  gap: 12px;
}

.format-notice {
  margin: 18px 0 0;
  padding: 10px 12px;
  border: 1px solid #d8e2f1;
  border-radius: 8px;
  background: #f8fbff;
  color: #475569;
  font-size: 13px;
  line-height: 1.6;
}

.summary-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(130px, 1fr));
  gap: 12px;
  margin: 22px 0;
}

.summary-card {
  border-radius: 8px;
  padding: 16px;
  border: 1px solid #e8edf5;
  background: #f8fafc;
}

.summary-card span {
  display: block;
  font-size: 13px;
  color: #64748b;
}

.summary-card strong {
  display: block;
  margin-top: 8px;
  font-size: 28px;
  color: #182230;
}

.summary-card.high {
  background: #fff5f5;
  border-color: #ffd6d6;
}

.summary-card.medium {
  background: #fff9ed;
  border-color: #ffe1ad;
}

.summary-card.low {
  background: #f1fbf4;
  border-color: #cdeed6;
}

.summary-card.na {
  background: #f8fafc;
  border-color: #cbd5e1;
}

.summary-card.source {
  background: #f7f5ff;
  border-color: #ddd6fe;
}

.summary-card.issue {
  background: #f0f9ff;
  border-color: #bae6fd;
}

.summary-card.must {
  background: #fef2f2;
  border-color: #fecaca;
}

.summary-card.must strong { color: #dc2626; }

.summary-card.suggest {
  background: #fff7ed;
  border-color: #fed7aa;
}

.summary-card.suggest strong { color: #ea580c; }

.summary-card.consider {
  background: #f0fdf4;
  border-color: #bbf7d0;
}

.summary-card.consider strong { color: #16a34a; }

.core-risk-panel {
  margin: 0 0 22px;
  padding: 16px;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  background: #ffffff;
}

.section-title {
  font-size: 15px;
  font-weight: 700;
  color: #1f2937;
  margin-bottom: 12px;
}

.core-risk-list {
  display: grid;
  gap: 10px;
}

.core-risk-row {
  display: grid;
  grid-template-columns: auto 1fr;
  align-items: start;
  gap: 10px;
  padding: 10px;
  border: 1px solid #eef2f7;
  border-radius: 8px;
  background: #f8fafc;
}

.core-risk-row p {
  margin: 4px 0 0;
  color: #475569;
  line-height: 1.6;
}

.empty-core-risk {
  color: #64748b;
  font-size: 14px;
}

/* 用户风险画像面板 */
.profile-panel {
  border: 1px solid #e8edf5;
  border-radius: 8px;
  overflow: hidden;
  margin-bottom: 12px;
}

.profile-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px 14px;
  background: #f8fafc;
  cursor: pointer;
  user-select: none;
}

.profile-header:hover {
  background: #f1f5f9;
}

.profile-title {
  font-size: 13px;
  font-weight: 600;
  color: #334155;
}

.profile-header .el-icon {
  transition: transform 0.25s;
}

.profile-header .el-icon.rotated {
  transform: rotate(180deg);
}

.profile-body {
  padding: 12px 14px;
  border-top: 1px solid #e8edf5;
}

.preset-row {
  display: flex;
  gap: 6px;
  margin-bottom: 10px;
}

.preset-row .el-button {
  flex: 1;
  font-size: 12px;
}

.profile-form {
  margin-top: 0;
}

.profile-form .el-form-item {
  margin-bottom: 8px;
}

/* 画像摘要 */
.profile-summary {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 14px;
  margin-bottom: 10px;
  border-radius: 8px;
  background: linear-gradient(135deg, #eff6ff, #f0f9ff);
  border: 1px solid #bfdbfe;
}

.profile-summary-header {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 13px;
  font-weight: 600;
  color: #1e40af;
  white-space: nowrap;
}

.profile-summary-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
}

/* 视图模式切换 */
.view-mode-switch {
  margin-bottom: 8px;
}

/* 诉讼分析样式 */
.litigation-disclaimer {
  display: flex;
  align-items: flex-start;
  gap: 8px;
  padding: 12px 16px;
  margin-bottom: 14px;
  border-radius: 8px;
  background: #fff7ed;
  border: 1px solid #fed7aa;
  font-size: 13px;
  color: #9a3412;
  line-height: 1.5;
}

.litigation-disclaimer .el-icon {
  margin-top: 2px;
  flex-shrink: 0;
}

.gap-list {
  list-style: none;
  padding: 0;
  margin: 4px 0 0;
}

.gap-list li {
  padding: 6px 10px;
  margin-bottom: 4px;
  border-radius: 6px;
  font-size: 13px;
  line-height: 1.5;
}

.gap-critical {
  background: #fef2f2;
  border-left: 3px solid #dc2626;
}

.gap-recommended {
  background: #fffbeb;
  border-left: 3px solid #f59e0b;
}

.gap-sufficient {
  background: #f0fdf4;
  border-left: 3px solid #16a34a;
}

.gap-hint {
  margin-top: 2px;
  font-size: 12px;
  color: #64748b;
}

.prediction-section {
  border-top: 1px solid #e8edf5;
  padding-top: 8px;
}

.prediction-row {
  margin-bottom: 6px;
  font-size: 13px;
  line-height: 1.6;
}

.prediction-row code {
  font-size: 12px;
  background: #f1f5f9;
  padding: 1px 6px;
  border-radius: 4px;
}

.pred-label {
  color: #64748b;
  font-weight: 500;
}

.cost-section {
  border-top: 1px solid #e8edf5;
  padding-top: 8px;
}

.cost-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 8px;
  margin-bottom: 10px;
}

.cost-item {
  padding: 10px;
  border-radius: 6px;
  background: #f8fafc;
  border: 1px solid #e8edf5;
}

.cost-label {
  display: block;
  font-size: 12px;
  color: #64748b;
  margin-bottom: 4px;
}

.cost-item strong {
  font-size: 16px;
  color: #182230;
}

.recommendation-badge {
  padding: 10px 14px;
  border-radius: 8px;
  font-size: 14px;
}

.recommendation-badge p {
  margin: 4px 0 0;
  font-size: 13px;
  color: #475569;
}

.recommendation-badge.建议起诉 {
  background: #dcfce7;
  border: 1px solid #86efac;
}

.recommendation-badge.建议起诉 strong {
  color: #16a34a;
}

.recommendation-badge.建议协商 {
  background: #fff7ed;
  border: 1px solid #fdba74;
}

.recommendation-badge.建议协商 strong {
  color: #ea580c;
}

.recommendation-badge.不建议起诉 {
  background: #fef2f2;
  border: 1px solid #fca5a5;
}

.recommendation-badge.不建议起诉 strong {
  color: #dc2626;
}

.litigation-item .item-body dt {
  margin-top: 10px;
  font-size: 14px;
  font-weight: 600;
}

/* 商业谈判样式 */
.negotiation-strategy {
  padding: 16px 20px;
  margin-bottom: 14px;
  border-radius: 10px;
  background: linear-gradient(135deg, #f0f9ff, #ecfdf5);
  border: 1px solid #bae6fd;
  font-size: 14px;
  line-height: 1.8;
}

.negotiation-strategy h3 {
  margin: 12px 0 6px;
  font-size: 16px;
  color: #1e40af;
}

.negotiation-strategy h4 {
  margin: 8px 0 4px;
  font-size: 14px;
  color: #334155;
}

.negotiation-strategy li {
  margin-bottom: 4px;
}

.intent-box {
  padding: 10px 14px;
  border-radius: 8px;
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  font-size: 13px;
  line-height: 1.7;
}

.intent-box div {
  margin-bottom: 4px;
}

.alternative-item {
  padding: 10px 14px;
  margin-bottom: 8px;
  border-radius: 8px;
  background: #f0fdf4;
  border: 1px solid #bbf7d0;
}

.alt-proposal {
  font-size: 13px;
  line-height: 1.6;
  margin-bottom: 6px;
}

.alt-meta {
  display: flex;
  gap: 6px;
}

.tradeoff-box {
  padding: 10px 14px;
  border-radius: 8px;
  background: #fffbeb;
  border: 1px solid #fde68a;
  font-size: 13px;
  line-height: 1.7;
}

.tradeoff-row {
  margin-bottom: 4px;
}

.give-label {
  color: #dc2626;
  font-weight: 500;
}

.ask-label {
  color: #16a34a;
  font-weight: 500;
}

.tradeoff-row.rationale {
  margin-top: 6px;
  padding-top: 6px;
  border-top: 1px dashed #fde68a;
  color: #92400e;
  font-style: italic;
}

.script-box {
  padding: 12px 16px;
  border-radius: 8px;
  background: #faf5ff;
  border: 1px solid #e9d5ff;
  border-left: 4px solid #8b5cf6;
  font-size: 14px;
  line-height: 1.8;
  color: #4c1d95;
}

.negotiation-item .item-body dt {
  margin-top: 12px;
  font-size: 14px;
  font-weight: 600;
}

/* 跨地域裁判预判样式 */
.jurisdiction-header {
  margin-bottom: 12px;
}

.jurisdiction-summary-box {
  display: flex;
  align-items: flex-start;
  gap: 8px;
  padding: 12px 16px;
  margin-bottom: 14px;
  border-radius: 8px;
  background: #eff6ff;
  border: 1px solid #bfdbfe;
  font-size: 13px;
  color: #1e40af;
  line-height: 1.6;
}

.jurisdiction-summary-box .el-icon {
  margin-top: 2px;
  flex-shrink: 0;
}

.tendency-box {
  padding: 12px 16px;
  border-radius: 8px;
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-left: 4px solid #3b82f6;
  font-size: 14px;
  line-height: 1.7;
}

.legal-basis-box {
  padding: 8px 12px;
  border-radius: 6px;
  background: #f1f5f9;
  font-size: 13px;
  color: #475569;
}

.case-item {
  padding: 10px 14px;
  margin-bottom: 8px;
  border-radius: 8px;
  background: #fefce8;
  border: 1px solid #fef08a;
}

.case-header {
  font-weight: 600;
  font-size: 13px;
  color: #854d0e;
  margin-bottom: 4px;
}

.case-court {
  font-size: 12px;
  color: #a16207;
  margin-bottom: 4px;
}

.case-conclusion {
  font-size: 13px;
  color: #334155;
  line-height: 1.6;
  margin-bottom: 4px;
}

.case-relevance {
  font-size: 12px;
  color: #64748b;
  font-style: italic;
}

.jurisdiction-tip-box {
  padding: 10px 14px;
  border-radius: 8px;
  background: #fef2f2;
  border: 1px solid #fecaca;
  border-left: 4px solid #ef4444;
  font-size: 13px;
  line-height: 1.6;
  color: #991b1b;
}

.data-source-note {
  margin-top: 8px;
  padding: 6px 10px;
  border-radius: 6px;
  background: #f8fafc;
  font-size: 12px;
  color: #94a3b8;
  font-style: italic;
}

.jurisdiction-item .item-body dt {
  margin-top: 12px;
  font-size: 14px;
  font-weight: 600;
}

.global-fallback {
  margin: -8px 0 18px;
  padding: 10px 12px;
  border-radius: 8px;
  color: #92400e;
  background: #fffbeb;
  border: 1px solid #fde68a;
  font-size: 13px;
  line-height: 1.6;
}

.review-list {
  display: grid;
  gap: 14px;
}

.coverage-filter,
.issue-filter,
.source-filter {
  width: 150px;
}

.source-filter {
  width: 132px;
}

.review-item {
  border: 1px solid #e6eaf2;
  border-radius: 8px;
  padding: 18px;
  background: #fff;
}

.item-title {
  font-size: 16px;
  font-weight: 700;
  color: #1f2937;
}

.item-body {
  margin: 16px 0;
}

.item-body dt {
  font-size: 13px;
  font-weight: 700;
  color: #334155;
  margin-top: 12px;
}

.item-body dd {
  margin: 6px 0 0;
  color: #475569;
  line-height: 1.7;
}

.fallback-reason {
  color: #b45309;
}

.evidence-list {
  display: grid;
  gap: 8px;
}

.evidence-item {
  border: 1px solid #e8edf5;
  border-radius: 6px;
  background: #f8fafc;
  padding: 8px 10px;
}

.evidence-item summary {
  cursor: pointer;
  color: #1f6feb;
  font-weight: 600;
}

.evidence-item p {
  margin: 8px 0 0;
  color: #334155;
  white-space: pre-wrap;
}

.no-evidence {
  color: #94a3b8;
}

.reasoning-chain {
  margin: 0;
  border: 1px solid #e8edf5;
  border-radius: 6px;
  background: #f8fafc;
  color: #334155;
  font-family: inherit;
  font-size: 13px;
  line-height: 1.8;
  padding: 10px 12px;
  white-space: pre-wrap;
  word-break: break-word;
}

.citation-list {
  margin: 0;
  padding-left: 18px;
  color: #334155;
}

.citation-list li + li {
  margin-top: 4px;
}

.review-controls {
  gap: 12px;
  border-top: 1px solid #edf1f7;
  padding-top: 14px;
}

.note-input {
  flex: 1;
}

.empty-icon {
  font-size: 80px;
  color: #b7c2d2;
}

@media (max-width: 980px) {
  .review-shell {
    grid-template-columns: 1fr;
  }

  .summary-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }

  .report-toolbar,
  .toolbar-actions,
  .review-controls {
    align-items: stretch;
    flex-direction: column;
  }
}
</style>
