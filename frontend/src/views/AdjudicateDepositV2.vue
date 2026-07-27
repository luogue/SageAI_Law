<template>
  <div class="deposit-v2-page">
    <section class="workspace">
      <div class="editor-panel">
        <div class="panel-header">
          <div>
            <p class="eyebrow">第二版</p>
            <h1>租赁合同纠纷裁判引擎</h1>
          </div>
          <el-tag effect="plain" type="warning">独立入口</el-tag>
        </div>

        <el-radio-group v-model="contractType" class="type-switch">
          <el-radio-button
            v-for="option in contractTypeOptions"
            :key="option.value"
            :label="option.value"
          >
            {{ option.label }}
          </el-radio-button>
        </el-radio-group>

        <el-input
          v-model="caseText"
          type="textarea"
          :rows="14"
          resize="none"
          maxlength="3000"
          show-word-limit
          :placeholder="placeholderText"
        />

        <div class="actions">
          <el-button :icon="DocumentCopy" @click="fillExample">填入示例</el-button>
          <el-button :icon="RefreshLeft" @click="resetAll">清空</el-button>
          <el-button type="primary" :icon="ScaleToOriginal" :loading="loading" @click="runEngine">
            {{ loading ? '裁判中' : '运行裁判引擎' }}
          </el-button>
        </div>
      </div>

      <div class="result-panel">
        <template v-if="result">
          <div class="verdict-box" :class="verdictClass">
            <div class="verdict-title">结论</div>
            <div class="verdict-text">{{ result.conclusion }}</div>
          </div>

          <el-tabs model-value="reasoning" class="result-tabs">
            <el-tab-pane label="三段式裁判" name="reasoning">
              <div class="reasoning-block">
                <h3>大前提（法条依据）</h3>
                <p>{{ result.major_premise }}</p>
              </div>
              <div class="reasoning-block">
                <h3>小前提（认定事实）</h3>
                <p>{{ result.minor_premise }}</p>
              </div>
              <div class="reasoning-block">
                <h3>结论（判决结果）</h3>
                <p>{{ result.conclusion }}</p>
              </div>
            </el-tab-pane>

            <el-tab-pane label="触发清单" name="patches">
              <div v-if="result.triggered_patches.length" class="patch-list">
                <el-tag
                  v-for="patch in result.triggered_patches"
                  :key="patch"
                  effect="plain"
                  type="warning"
                  size="large"
                >
                  {{ patch }}
                </el-tag>
              </div>
              <el-empty v-else description="本案未触发前置模块或特殊规则" />
            </el-tab-pane>

            <el-tab-pane label="抽取事实" name="facts">
              <dl class="facts-grid">
                <template v-for="item in factItems" :key="item.label">
                  <dt>{{ item.label }}</dt>
                  <dd>{{ item.value }}</dd>
                </template>
              </dl>
            </el-tab-pane>

            <el-tab-pane label="路径" name="path">
              <el-timeline>
                <el-timeline-item v-for="step in result.path" :key="step">
                  {{ step }}
                </el-timeline-item>
              </el-timeline>
            </el-tab-pane>
          </el-tabs>
        </template>

        <el-empty v-else description="输入自然语言案件事实后运行裁判引擎">
          <template #image>
            <el-icon :size="72" color="#b8c0cc"><ScaleToOriginal /></el-icon>
          </template>
        </el-empty>
      </div>
    </section>
  </div>
</template>

<script setup>
import { computed, ref } from 'vue'
import { ElMessage } from 'element-plus'
import { DocumentCopy, RefreshLeft, ScaleToOriginal } from '@element-plus/icons-vue'
import { adjudicateDepositV2 } from '@/api/adjudicate'

const exampleText = '租赁期间出售房屋，新房主要求租客马上搬走。租客在房屋出售前已经签订租赁合同并入住，询问是否必须搬走以及押金如何处理。'

const contractType = ref('house')
const caseText = ref('')
const loading = ref(false)
const result = ref(null)

const contractTypeOptions = [
  { label: '房屋租赁', value: 'house' },
  { label: '车辆租赁', value: 'vehicle' },
  { label: '设备租赁', value: 'equipment' },
]

const placeholderText = computed(() => {
  const examples = {
    house: '请输入案件事实。例如：租赁期间出售房屋，新房主要求租客搬走。或：合同期满后租客继续居住、房东继续收租但未续签合同。',
    vehicle: '请输入案件事实。例如：车辆租期到期后承租人继续使用车辆，出租人继续收租，双方未签新合同。或：承租人提前还车，出租人要求扣押金。',
    equipment: '请输入案件事实。例如：设备交付前已有故障，承租方要求减租。或：设备租期届满后继续使用，出租方照常收租但未续签合同。',
  }
  return examples[contractType.value]
})

const verdictClass = computed(() => {
  const text = result.value?.conclusion || ''
  if (text.includes('全额返还')) return 'is-return'
  if (text.includes('扣除')) return 'is-deduct'
  if (text.includes('驳回') || text.includes('不适用')) return 'is-reject'
  return 'is-review'
})

const factItems = computed(() => {
  const facts = result.value?.facts || {}
  return [
    ['第三方介入', boolText(facts.has_third_party)],
    ['合同类型', facts.contract_type_name || '未识别'],
    ['承租人死亡', boolText(facts.tenant_dead)],
    ['共同居住/经营人', boolText(facts.cohabitant_or_cooperator)],
    ['情势变更', boolText(facts.changed_circumstances)],
    ['违法建筑', boolText(facts.illegal_building)],
    ['转租链条', boolText(facts.sublease_chain_dispute)],
    ['出租人死亡', boolText(facts.landlord_dead)],
    ['不定期租赁', boolText(facts.indefinite_lease)],
    ['期满继续居住', boolText(facts.tenant_continues_use_after_expiry)],
    ['继续收租/未异议', boolText(facts.landlord_collects_rent_or_no_objection)],
    ['未签新合同', boolText(facts.no_new_lease_contract)],
    ['询问管辖', boolText(facts.asks_jurisdiction)],
    ['询问被告', boolText(facts.asks_defendant)],
    ['解除合同', boolText(facts.termination_requested)],
    ['根本违约', boolText(facts.fundamental_breach)],
    ['房屋出售', boolText(facts.house_sold)],
    ['先租后卖', boolText(facts.lease_before_sale)],
    ['先卖后租', boolText(facts.sale_before_lease)],
    ['房屋瑕疵', boolText(Boolean(facts.pre_delivery_defect || facts.third_party_defect || facts.expropriation_or_demolition || facts.serious_safety_risk))],
    ['合同终止日期', facts.contract_end_date || '未识别'],
    ['合同有效性', facts.contract_valid === null ? '未识别' : boolText(facts.contract_valid)],
    ['非房东本人签署', boolText(facts.signer_not_landlord)],
    ['提前退租', boolText(facts.is_early_termination)],
    ['提前退租约定', boolText(facts.has_early_termination_clause)],
    ['存在损坏', facts.has_damage === null ? '未识别' : boolText(facts.has_damage)],
    ['损坏原因', reasonText(facts.damage_reason)],
    ['约定扣款', moneyText(facts.agreed_deduction)],
    ['实际损失', moneyText(facts.actual_loss)],
  ].map(([label, value]) => ({ label, value }))
})

function boolText(value) {
  return value ? '是' : '否'
}

function moneyText(value) {
  const number = Number(value || 0)
  return number > 0 ? `${number.toFixed(2)}元` : '未识别'
}

function reasonText(value) {
  const map = {
    natural_wear: '自然损耗',
    unproven: '无法证明原因',
    tenant_fault: '承租人过错',
  }
  return map[value] || '未识别'
}

function fillExample() {
  caseText.value = exampleText
}

function resetAll() {
  caseText.value = ''
  result.value = null
}

async function runEngine() {
  if (!caseText.value.trim()) {
    ElMessage.warning('请先输入案件事实')
    return
  }
  loading.value = true
  result.value = null
  try {
    result.value = await adjudicateDepositV2(caseText.value.trim(), contractType.value)
  } catch (error) {
    ElMessage.error(error.message || '裁判失败，请稍后重试')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.deposit-v2-page {
  flex: 1;
  background: #f6f7f9;
  padding: 24px;
}

.workspace {
  display: grid;
  grid-template-columns: minmax(360px, 0.95fr) minmax(420px, 1.05fr);
  gap: 20px;
  max-width: 1280px;
  margin: 0 auto;
  align-items: start;
}

.editor-panel,
.result-panel {
  background: #fff;
  border: 1px solid #e6e8ee;
  border-radius: 8px;
  padding: 20px;
  min-height: 560px;
}

.panel-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 16px;
  margin-bottom: 16px;
}

.eyebrow {
  margin: 0 0 4px;
  color: #b56b00;
  font-size: 13px;
  font-weight: 600;
}

h1 {
  margin: 0;
  color: #1f2937;
  font-size: 24px;
  line-height: 1.25;
}

.actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 16px;
  flex-wrap: wrap;
}

.type-switch {
  margin-bottom: 14px;
}

.verdict-box {
  border-radius: 8px;
  padding: 16px;
  margin-bottom: 16px;
  border: 1px solid;
}

.verdict-title {
  font-size: 13px;
  font-weight: 600;
  margin-bottom: 6px;
}

.verdict-text {
  color: #1f2937;
  font-size: 17px;
  font-weight: 700;
  line-height: 1.55;
}

.is-return {
  background: #f0f9eb;
  border-color: #d8edcd;
}

.is-deduct {
  background: #fff7ed;
  border-color: #fed7aa;
}

.is-reject {
  background: #f4f4f5;
  border-color: #dedfe3;
}

.is-review {
  background: #eef6ff;
  border-color: #cfe5ff;
}

.result-tabs {
  --el-color-primary: #1f6feb;
}

.reasoning-block {
  padding: 14px 0;
  border-bottom: 1px solid #eceff3;
}

.reasoning-block:last-child {
  border-bottom: none;
}

.reasoning-block h3 {
  margin: 0 0 8px;
  color: #374151;
  font-size: 15px;
}

.reasoning-block p {
  margin: 0;
  color: #4b5563;
  line-height: 1.75;
}

.patch-list {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  padding-top: 8px;
}

.facts-grid {
  display: grid;
  grid-template-columns: 150px 1fr;
  gap: 0;
  margin: 8px 0 0;
  border: 1px solid #eceff3;
  border-radius: 8px;
  overflow: hidden;
}

.facts-grid dt,
.facts-grid dd {
  margin: 0;
  padding: 10px 12px;
  border-bottom: 1px solid #eceff3;
}

.facts-grid dt {
  background: #fafafa;
  color: #606266;
  font-weight: 600;
}

.facts-grid dd {
  color: #1f2937;
}

.facts-grid dt:nth-last-of-type(1),
.facts-grid dd:nth-last-of-type(1) {
  border-bottom: none;
}

@media (max-width: 920px) {
  .deposit-v2-page {
    padding: 16px;
  }

  .workspace {
    grid-template-columns: 1fr;
  }

  .editor-panel,
  .result-panel {
    min-height: auto;
  }
}
</style>
