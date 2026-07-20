<template>
  <div class="adjudicate-page">
    <div class="page-header">
      <el-icon :size="24"><Money /></el-icon>
      <h1>租赁押金纠纷裁判</h1>
      <span class="page-desc">输入纠纷事实，智能生成裁判结果及法律依据</span>
    </div>

    <div class="main-content">
      <!-- 左侧：输入表单 -->
      <div class="form-panel">
        <el-card shadow="never" class="section-card">
          <template #header>
            <div class="card-title"><span class="step">1</span> 基本信息</div>
          </template>
          <el-form :model="form" label-width="110px" label-position="right">
            <el-row :gutter="20">
              <el-col :span="12">
                <el-form-item label="合同是否有效">
                  <el-switch v-model="form.contract_valid" active-text="有效" inactive-text="无效" />
                </el-form-item>
              </el-col>
              <el-col :span="12">
                <el-form-item label="合同终止日">
                  <el-date-picker v-model="form.contract_end_date" type="date" placeholder="选择日期"
                    value-format="YYYY-MM-DD" style="width:100%" />
                </el-form-item>
              </el-col>
            </el-row>
            <el-form-item label="合同条款">
              <el-tag v-for="(clause, i) in form.contract_clauses" :key="i" closable class="clause-tag"
                @close="form.contract_clauses.splice(i, 1)">{{ clause }}</el-tag>
              <el-input v-if="clauseInputVisible" ref="clauseInputRef" v-model="clauseInputValue" size="small"
                class="clause-input" @keyup.enter="addClause" @blur="addClause" />
              <el-button v-else size="small" @click="showClauseInput">+ 添加条款</el-button>
            </el-form-item>
          </el-form>
        </el-card>

        <el-card shadow="never" class="section-card">
          <template #header>
            <div class="card-title"><span class="step">2</span> 退租情况</div>
          </template>
          <el-form :model="form" label-width="110px" label-position="right">
            <el-row :gutter="20">
              <el-col :span="8">
                <el-form-item label="提前退租">
                  <el-switch v-model="form.is_early_termination" />
                </el-form-item>
              </el-col>
              <el-col :span="8">
                <el-form-item label="是否有损坏">
                  <el-switch v-model="form.has_damage" />
                </el-form-item>
              </el-col>
              <el-col :span="8">
                <el-form-item label="第三人侵权">
                  <el-switch v-model="form.has_third_party" />
                </el-form-item>
              </el-col>
            </el-row>
            <el-row :gutter="20" v-if="form.has_damage">
              <el-col :span="8">
                <el-form-item label="损坏原因">
                  <el-select v-model="form.damage_reason" placeholder="选择" clearable style="width:100%">
                    <el-option label="自然损耗" value="natural_wear" />
                    <el-option label="承租人过错" value="tenant_fault" />
                  </el-select>
                </el-form-item>
              </el-col>
              <el-col :span="8">
                <el-form-item label="损坏物类型">
                  <el-select v-model="form.damage_item" placeholder="选择" clearable style="width:100%">
                    <el-option label="装修加装物" value="decoration" />
                    <el-option label="一般家具家电" value="furniture" />
                    <el-option label="墙面地面" value="surface" />
                    <el-option label="其他" value="other" />
                  </el-select>
                </el-form-item>
              </el-col>
              <el-col :span="8">
                <el-form-item label="主张赔偿方">
                  <el-select v-model="form.damage_claimed_by" placeholder="选择" clearable style="width:100%">
                    <el-option label="房东" value="landlord" />
                    <el-option label="租客" value="tenant" />
                  </el-select>
                </el-form-item>
              </el-col>
            </el-row>
          </el-form>
        </el-card>

        <el-card shadow="never" class="section-card" v-if="form.has_damage">
          <template #header>
            <div class="card-title"><span class="step">3</span> 金额与举证</div>
          </template>
          <el-form :model="form" label-width="120px" label-position="right">
            <el-row :gutter="20">
              <el-col :span="12">
                <el-form-item label="合同约定扣款">
                  <el-input-number v-model="form.agreed_deduction" :min="0" :step="100" style="width:100%" />
                </el-form-item>
              </el-col>
              <el-col :span="12">
                <el-form-item label="实际维修报价">
                  <el-input-number v-model="form.repair_quote" :min="0" :step="100" style="width:100%" />
                </el-form-item>
              </el-col>
            </el-row>
            <el-row :gutter="20">
              <el-col :span="8">
                <el-form-item label="空置天数">
                  <el-input-number v-model="form.vacancy_days" :min="0" style="width:100%" />
                </el-form-item>
              </el-col>
              <el-col :span="8">
                <el-form-item label="日租金(元)">
                  <el-input-number v-model="form.daily_rent" :min="0" :step="10" style="width:100%" />
                </el-form-item>
              </el-col>
              <el-col :span="8">
                <el-form-item label="能否证明原因">
                  <el-switch v-model="form.evidence_can_prove_cause" />
                </el-form-item>
              </el-col>
            </el-row>
            <el-row :gutter="20">
              <el-col :span="12">
                <el-form-item label="租客有维修反诉">
                  <el-switch v-model="form.tenant_has_repair_claim" />
                </el-form-item>
              </el-col>
            </el-row>
          </el-form>
        </el-card>

        <el-card shadow="never" class="section-card">
          <template #header>
            <div class="card-title"><span class="step">4</span> 特殊情形</div>
          </template>
          <el-form :model="form" label-width="160px" label-position="right">
            <el-row :gutter="20">
              <el-col :span="12">
                <el-form-item label="入住时已告知瑕疵">
                  <el-switch v-model="form.notified_at_check_in" />
                </el-form-item>
              </el-col>
              <el-col :span="12">
                <el-form-item label="房东知情后沉默">
                  <el-switch v-model="form.landlord_remained_silent" />
                </el-form-item>
              </el-col>
            </el-row>
            <el-row :gutter="20">
              <el-col :span="12">
                <el-form-item label="房东知悉解除事由日期">
                  <el-date-picker v-model="form.landlord_know_date" type="date" placeholder="选择日期"
                    value-format="YYYY-MM-DD" style="width:100%" />
                </el-form-item>
              </el-col>
            </el-row>
          </el-form>
        </el-card>

        <div class="submit-area">
          <el-button type="primary" size="large" @click="handleSubmit" :loading="loading" :icon="Promotion">
            {{ loading ? '裁判中...' : '开始裁判' }}
          </el-button>
        </div>
      </div>

      <!-- 右侧：结果展示 -->
      <div class="result-panel">
        <el-card shadow="never" class="result-card" v-if="result">
          <template #header>
            <div class="card-title"><el-icon><Finished /></el-icon> 裁判结果</div>
          </template>

          <!-- 判决结论 -->
          <div class="verdict" :class="verdictClass">
            <el-icon :size="20">
              <SuccessFilled v-if="result.result.includes('全额返还')" />
              <WarningFilled v-else-if="result.result.includes('扣除')" />
              <CircleCloseFilled v-else-if="result.result.includes('驳回')" />
              <InfoFilled v-else />
            </el-icon>
            <span>{{ result.result }}</span>
          </div>

          <!-- 决策路径 -->
          <div class="result-section" v-if="result.path && result.path.length > 0">
            <h4><el-icon><Guide /></el-icon> 决策路径</h4>
            <div class="path-flow">
              <span v-for="(step, i) in result.path" :key="i" class="path-step">
                {{ step }}
                <el-icon v-if="i < result.path.length - 1" class="path-arrow"><ArrowRight /></el-icon>
              </span>
            </div>
          </div>

          <!-- 触发补丁 -->
          <div class="result-section" v-if="result.triggered_patches && result.triggered_patches.length > 0">
            <h4><el-icon><Switch /></el-icon> 触发法律补丁</h4>
            <div class="patches">
              <el-tag v-for="(p, i) in result.triggered_patches" :key="i" class="patch-tag"
                :type="patchType(p)" effect="plain" size="large">
                <el-icon><Check /></el-icon>
                {{ p }}
              </el-tag>
            </div>
          </div>
        </el-card>

        <!-- 空状态 -->
        <el-card shadow="never" class="result-card empty-card" v-else>
          <el-empty description="请在左侧填写纠纷事实后点击「开始裁判」">
            <template #image>
              <el-icon :size="80" color="#c0c4cc"><Document /></el-icon>
            </template>
          </el-empty>
        </el-card>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, nextTick } from 'vue'
import {
  Money, Promotion, Finished, Document, Guide, ArrowRight,
  Check, Switch, SuccessFilled, WarningFilled, CircleCloseFilled, InfoFilled
} from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import { adjudicateDeposit } from '@/api/adjudicate'

const loading = ref(false)
const result = ref(null)

const form = reactive({
  contract_valid: true,
  contract_end_date: '',
  contract_clauses: [],
  is_early_termination: false,
  has_damage: false,
  has_third_party: false,
  damage_reason: null,
  damage_item: null,
  damage_claimed_by: null,
  evidence_can_prove_cause: true,
  notified_at_check_in: false,
  landlord_remained_silent: false,
  landlord_know_date: '',
  agreed_deduction: 0,
  repair_quote: 0,
  vacancy_days: 0,
  daily_rent: 0,
  tenant_has_repair_claim: false,
})

// 合同条款标签输入
const clauseInputVisible = ref(false)
const clauseInputValue = ref('')
const clauseInputRef = ref(null)

function showClauseInput() {
  clauseInputVisible.value = true
  nextTick(() => clauseInputRef.value?.focus())
}

function addClause() {
  if (clauseInputValue.value.trim()) {
    form.contract_clauses.push(clauseInputValue.value.trim())
  }
  clauseInputVisible.value = false
  clauseInputValue.value = ''
}

// 判决样式
const verdictClass = computed(() => {
  if (!result.value) return ''
  const r = result.value.result
  if (r.includes('全额返还') || r.includes('无权扣款') || r.includes('退还')) return 'verdict-win'
  if (r.includes('扣除') || r.includes('不退还')) return 'verdict-lose'
  if (r.includes('驳回') || r.includes('终止')) return 'verdict-deny'
  return 'verdict-info'
})

function patchType(patch) {
  if (patch.startsWith('P1') || patch.startsWith('P2')) return 'warning'
  if (patch.startsWith('P3') || patch.startsWith('P4') || patch.startsWith('P5')) return 'danger'
  if (patch.startsWith('P6') || patch.startsWith('P7')) return ''
  if (patch.includes('隐性')) return 'success'
  return ''
}

async function handleSubmit() {
  loading.value = true
  result.value = null
  try {
    const payload = {
      contract_valid: form.contract_valid,
      contract_end_date: form.contract_end_date || null,
      contract_clauses: form.contract_clauses.length > 0 ? form.contract_clauses : null,
      is_early_termination: form.is_early_termination,
      has_damage: form.has_damage,
      has_third_party: form.has_third_party,
      damage_reason: form.damage_reason || null,
      damage_item: form.damage_item || null,
      damage_claimed_by: form.damage_claimed_by || null,
      evidence_can_prove_cause: form.evidence_can_prove_cause,
      notified_at_check_in: form.notified_at_check_in,
      landlord_remained_silent: form.landlord_remained_silent,
      landlord_know_date: form.landlord_know_date || null,
      agreed_deduction: form.agreed_deduction,
      repair_quote: form.repair_quote,
      vacancy_days: form.vacancy_days,
      daily_rent: form.daily_rent,
      tenant_has_repair_claim: form.tenant_has_repair_claim,
    }
    const data = await adjudicateDeposit(payload)
    result.value = data
  } catch (err) {
    ElMessage.error(err.message || '裁判失败，请稍后重试')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.adjudicate-page {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.page-header {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 24px;
  flex-wrap: wrap;
}
.page-header h1 {
  margin: 0;
  font-size: 22px;
  color: #303133;
}
.page-desc {
  color: #909399;
  font-size: 14px;
  margin-left: 8px;
}

.main-content {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 24px;
  align-items: start;
}

.section-card, .result-card {
  margin-bottom: 16px;
}
.card-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 600;
  font-size: 15px;
}
.step {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 22px;
  height: 22px;
  border-radius: 50%;
  background: #409eff;
  color: #fff;
  font-size: 12px;
  font-weight: 700;
}

/* 合同条款标签 */
.clause-tag { margin-right: 6px; margin-bottom: 4px; }
.clause-input { width: 120px; display: inline-block; }

.submit-area {
  text-align: center;
  padding: 20px 0;
}

/* 判决结论 */
.verdict {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 16px 20px;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 600;
  margin-bottom: 20px;
  line-height: 1.6;
}
.verdict-win  { background: #f0f9eb; color: #67c23a; border: 1px solid #e1f3d8; }
.verdict-lose { background: #fef0f0; color: #e6a23c; border: 1px solid #fde2e2; }
.verdict-deny { background: #f4f4f5; color: #909399; border: 1px solid #e9e9eb; }
.verdict-info { background: #ecf5ff; color: #409eff; border: 1px solid #d9ecff; }

/* 决策路径 */
.result-section { margin-bottom: 16px; }
.result-section h4 { display: flex; align-items: center; gap: 6px; font-size: 14px; color: #606266; margin: 0 0 10px 0; }

.path-flow {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 4px;
  padding: 10px 14px;
  background: #f5f7fa;
  border-radius: 6px;
  font-size: 13px;
  color: #606266;
}
.path-arrow { color: #c0c4cc; margin: 0 2px; }

/* 触发补丁 */
.patches {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}
.patch-tag { font-size: 13px; }

.empty-card {
  min-height: 300px;
  display: flex;
  align-items: center;
  justify-content: center;
}

@media (max-width: 860px) {
  .main-content {
    grid-template-columns: 1fr;
  }
}
</style>
