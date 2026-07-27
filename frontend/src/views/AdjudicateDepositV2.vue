<template>
  <div class="deposit-v2-page">
    <section class="workspace">
      <div class="editor-panel">
        <div class="panel-header">
          <div>
            <p class="eyebrow">第二版</p>
            <h1>合同纠纷裁判引擎</h1>
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

const exampleTexts = {
  house: '租赁期间出售房屋，新房主要求租客马上搬走。租客在房屋出售前已经签订租赁合同并入住，询问是否必须搬走以及押金如何处理。',
  vehicle: '车辆因承租人原因损坏，正在维修，出租人主张停运损失。日租金300元，维修5天。',
  equipment: '设备故障后承租方未及时通知出租方，仍继续使用，导致损失扩大，损失8000元。',
  property_management: '物业起诉追缴2020年1月至2021年12月、2024年1月至2024年6月物业费，业主抗辩物业多处服务不达标。',
  transportation: '托运人将货物交给承运人后，货物在运输过程中灭失，承运人无法证明免责事由，货值10000元。',
  work_contract: '承揽人已交付工作成果，但质量不合格，瑕疵轻微可修复，定作人要求修理。',
  deposit: '有偿保管期间保管物丢失，保管人未尽妥善保管义务，物品价值10000元。',
  sale: '买受人收到货物后发现质量不合格，已在合理期限内通知出卖人，瑕疵严重导致合同目的不能实现，买受人要求解除合同。',
  agency: '有偿委托中，受托人未按委托人指示办理事务，造成实际损失5000元，委托人要求受托人赔偿。',
  loan: '民间借贷中借条金额100万元，借款人实际到账95万元，5万元为预扣利息，双方约定年利率18%，一年期LPR为3.85%。',
  service: '消费者预付式消费办卡充值5000元，健身房停业并恶意逃避退款，消费者要求退还预付款并主张惩罚性赔偿。',
}

const contractType = ref('house')
const caseText = ref('')
const loading = ref(false)
const result = ref(null)

const contractTypeOptions = [
  { label: '房屋租赁', value: 'house' },
  { label: '车辆租赁', value: 'vehicle' },
  { label: '设备租赁', value: 'equipment' },
  { label: '物业服务', value: 'property_management' },
  { label: '运输合同', value: 'transportation' },
  { label: '承揽合同', value: 'work_contract' },
  { label: '保管合同', value: 'deposit' },
  { label: '买卖合同', value: 'sale' },
  { label: '委托合同', value: 'agency' },
  { label: '借款合同', value: 'loan' },
  { label: '服务合同', value: 'service' },
]

const placeholderText = computed(() => {
  const examples = {
    house: '请输入案件事实。例如：租赁期间出售房屋，新房主要求租客搬走。或：合同期满后租客继续居住、房东继续收租但未续签合同。',
    vehicle: '请输入案件事实。例如：车辆租期到期后承租人继续使用车辆，出租人继续收租，双方未签新合同。或：承租人提前还车，出租人要求扣押金。',
    equipment: '请输入案件事实。例如：设备交付前已有故障，承租方要求减租。或：设备租期届满后继续使用，出租方照常收租但未续签合同。',
    property_management: '请输入案件事实。例如：物业起诉追缴多期物业费，业主抗辩服务不达标。或：物业以停水停电方式催缴物业费。',
    transportation: '请输入案件事实。例如：货物在运输过程中毁损、灭失，承运人是否能证明免责事由。或：托运人未付运费，承运人主张留置货物。',
    work_contract: '请输入案件事实。例如：工作成果质量不合格，定作人要求修理、重作、减少报酬或赔偿损失。或：定作人完成前解除合同。',
    deposit: '请输入案件事实。例如：保管物在保管期间丢失，保管合同是有偿还是无偿，保管人是否妥善保管。或：寄存人要求领取保管物，保管人拒绝返还。',
    sale: '请输入案件事实。例如：标的物交付前毁损灭失，风险由谁承担。或：货物质量不符合约定，买受人是否及时提出异议以及可选择何种救济。',
    agency: '请输入案件事实。例如：受托人是否按指示处理事务、是否有偿、是否越权、是否转委托、是否取得财产未转交，或委托人是否拖欠费用报酬。',
    loan: '请输入案件事实。例如：借条金额与实际到账是否一致、利率和LPR是多少、是否已还款、是否提前还款、是否展期、保证人是否应担责。',
    service: '请输入案件事实。例如：预付式消费是否停业退款、服务质量是否达标、是否不退不换格式条款、健康原因能否解除，或平台是否单方变更服务条款。',
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
    ['物业费争议', boolText(facts.property_fee_dispute)],
    ['物业服务瑕疵', boolText(facts.service_defect)],
    ['瑕疵程度', propertyDefectText(facts)],
    ['非法催收', boolText(facts.illegal_collection)],
    ['解聘争议', boolText(facts.dismissal_dispute)],
    ['公共收益争议', boolText(facts.public_income_dispute)],
    ['公共收益金额', moneyText(facts.public_income_amount)],
    ['事实物业关系', boolText(Boolean(facts.no_written_contract && facts.actual_property_service))],
    ['物业合同终止', boolText(facts.contract_terminated)],
    ['原物业拒退/交接', boolText(Boolean(facts.original_property_refuses_exit || facts.original_property_refuses_handover))],
    ['物业撤销解聘诉讼', boolText(facts.property_company_challenges_dismissal)],
    ['货损/灭失', boolText(Boolean(facts.cargo_damage || facts.cargo_loss))],
    ['延迟交付', boolText(facts.cargo_delay)],
    ['运输过程中', boolText(facts.in_transit)],
    ['承运人证明免责', boolText(facts.carrier_proves_exemption)],
    ['保价/限额条款', boolText(facts.valuation_clause)],
    ['多式联运', boolText(facts.continuous_transport)],
    ['留置权争议', boolText(Boolean(facts.unpaid_freight || facts.lien_claim))],
    ['同一法律关系', boolText(facts.same_legal_relationship)],
    ['排除留置约定', boolText(facts.lien_excluded_by_contract)],
    ['运输区段不明', boolText(facts.unknown_transport_segment)],
    ['货物市场价值', moneyText(facts.market_price)],
    ['延迟损失', moneyText(facts.delay_loss)],
    ['承揽合同关系', boolText(facts.work_contract)],
    ['合同定性争议', boolText(facts.contract_nature_dispute)],
    ['工作成果已交付', boolText(facts.result_delivered)],
    ['工作成果未交付', boolText(facts.not_delivered)],
    ['质量瑕疵', boolText(facts.quality_defect)],
    ['质量合格', boolText(facts.quality_conform)],
    ['瑕疵程度', workDefectText(facts)],
    ['定作人解除', boolText(facts.customer_termination)],
    ['转包/分包', boolText(Boolean(facts.main_work_subcontract || facts.auxiliary_subcontract))],
    ['违法转包', boolText(Boolean(facts.total_subcontract || facts.disassembled_subcontract))],
    ['接近完成/大额投入', boolText(Boolean(facts.near_completion || facts.substantial_cost_invested))],
    ['定作人协助缺失', boolText(facts.customer_assistance_missing)],
    ['定作人变更要求', boolText(facts.customer_change_request)],
    ['材料瑕疵', boolText(facts.customer_material_defect)],
    ['保管损坏', boolText(facts.custody_damage)],
    ['承揽报酬', moneyText(facts.remuneration_amount)],
    ['保管合同关系', boolText(facts.safekeeping_contract)],
    ['保管合同定性争议', boolText(facts.contract_nature_dispute)],
    ['保管物交付', boolText(facts.item_delivered)],
    ['保管期间损失', boolText(Boolean(facts.item_damage || facts.item_loss || facts.non_return))],
    ['有偿保管', boolText(facts.paid_safekeeping)],
    ['无偿保管', boolText(facts.unpaid_safekeeping)],
    ['保管不善', boolText(facts.improper_custody)],
    ['转保管', boolText(facts.transfer_to_third)],
    ['擅自使用保管物', boolText(Boolean(facts.custodian_used_item || facts.third_party_use))],
    ['贵重物品未声明', boolText(Boolean(facts.valuable_item && facts.undeclared_valuable))],
    ['消费保管', boolText(facts.consumptive_safekeeping)],
    ['保管人留置', boolText(Boolean(facts.unpaid_fee || facts.lien_claim))],
    ['逾期领取', boolText(facts.depositor_overdue_retrieval)],
    ['买卖合同关系', boolText(facts.sale_contract)],
    ['无书面合同', boolText(facts.no_written_contract)],
    ['分期付款买卖', boolText(facts.installment_sale)],
    ['试用买卖', boolText(facts.trial_sale)],
    ['所有权保留', boolText(facts.title_retention)],
    ['凭样品买卖', boolText(facts.sample_sale)],
    ['电子信息产品', boolText(facts.electronic_product)],
    ['多交标的物', boolText(facts.over_delivery)],
    ['标的物交付', boolText(facts.delivered)],
    ['风险损失', boolText(facts.risk_loss)],
    ['质量瑕疵', boolText(facts.quality_nonconform)],
    ['权利瑕疵', boolText(facts.third_party_right)],
    ['一物数卖', boolText(facts.multi_sale)],
    ['未付价款', moneyText(facts.unpaid_price)],
    ['可得利益', moneyText(facts.expected_profit)],
    ['委托合同关系', boolText(facts.agency_contract)],
    ['委托定性争议', boolText(facts.nature_dispute)],
    ['处理委托事务', boolText(facts.process_affairs)],
    ['有偿委托', boolText(facts.paid_agency)],
    ['无偿委托', boolText(facts.unpaid_agency)],
    ['特别/概括委托', agencyScopeText(facts)],
    ['费用报酬争议', boolText(Boolean(facts.expense_advance || facts.remuneration_unpaid))],
    ['受托人越权', boolText(facts.over_authority)],
    ['受托人过错损失', boolText(Boolean(facts.trustee_loss || facts.trustee_fault))],
    ['转委托', boolText(facts.sub_entrustment)],
    ['自己/双方代理', boolText(Boolean(facts.self_agency || facts.both_side_agency))],
    ['未报告/虚假报告', boolText(Boolean(facts.report_failure || facts.false_report))],
    ['取得财产未转交', boolText(facts.property_not_transferred)],
    ['隐名委托交易', boolText(Boolean(facts.trustee_own_name || facts.third_party_unknown_agency))],
    ['介入/选择抗辩', boolText(facts.defense_continuation)],
    ['任意解除', boolText(facts.arbitrary_termination)],
    ['共同受托人', boolText(facts.joint_trustees)],
    ['委托终止事由', boolText(Boolean(facts.principal_dead_or_terminated || facts.trustee_dead_or_incapable))],
    ['借款合同关系', boolText(facts.loan_contract)],
    ['金融机构出借', boolText(facts.financial_institution_lender)],
    ['民间借贷', boolText(facts.private_lender)],
    ['自然人间借款', boolText(facts.natural_person_loan)],
    ['实际提供借款', boolText(facts.loan_provided)],
    ['合同无效争议', boolText(Boolean(facts.contract_invalid || facts.relending_bank_loan || facts.professional_lender_claim))],
    ['职业放贷争议', boolText(facts.professional_lender_claim)],
    ['企业间借贷', boolText(facts.enterprise_loan)],
    ['仅有转账凭证', boolText(facts.only_transfer_record)],
    ['债权凭证未载明债权人', boolText(facts.voucher_no_creditor)],
    ['砍头息', boolText(facts.deducted_interest)],
    ['名义本金', moneyText(facts.nominal_principal)],
    ['实际到账', moneyText(facts.actual_received)],
    ['部分还款', boolText(facts.partial_repayment)],
    ['还款金额', moneyText(facts.repayment_amount)],
    ['约定利息', boolText(facts.interest_agreed)],
    ['无利息约定', boolText(facts.no_interest_agreed)],
    ['年利率', percentText(facts.annual_rate)],
    ['一年期LPR', percentText(facts.lpr_rate)],
    ['提前还款', boolText(facts.early_repayment)],
    ['借款展期', boolText(facts.extension_request)],
    ['保证责任', boolText(facts.guarantee_contract)],
    ['借新还旧', boolText(facts.loan_old_for_new)],
    ['夫妻共同债务', boolText(facts.spousal_debt)],
    ['未按用途使用借款', boolText(facts.misuse_loan)],
    ['服务合同关系', boolText(facts.service_contract)],
    ['服务定性争议', boolText(facts.nature_dispute)],
    ['预付式消费', boolText(facts.prepaid_consumption)],
    ['消费者身份', boolText(facts.consumer)],
    ['经营者停业', boolText(facts.operator_closed)],
    ['恶意逃避退款', boolText(facts.malicious_refund_evasion)],
    ['预付款金额', moneyText(facts.prepaid_amount)],
    ['未消费/剩余金额', moneyText(facts.unused_amount)],
    ['服务未提供', boolText(facts.service_not_provided)],
    ['服务部分提供', boolText(facts.service_partly_provided)],
    ['不退不换条款', boolText(facts.format_no_refund)],
    ['服务单方变更', boolText(facts.provider_unilateral_change)],
    ['服务质量争议', boolText(Boolean(facts.service_quality_dispute || facts.quality_nonconform))],
    ['资质/人员不符', boolText(Boolean(facts.provider_no_qualification || facts.staff_mismatch))],
    ['健康原因解除', boolText(facts.health_change)],
    ['不定期服务', boolText(facts.indefinite_service)],
    ['平台条款变更', boolText(facts.platform_terms_change)],
    ['经营业务转让', boolText(facts.business_transfer)],
    ['保过承诺', boolText(facts.guaranteed_result)],
  ].map(([label, value]) => ({ label, value }))
})

function boolText(value) {
  return value ? '是' : '否'
}

function moneyText(value) {
  const number = Number(value || 0)
  return number > 0 ? `${number.toFixed(2)}元` : '未识别'
}

function percentText(value) {
  const number = Number(value || 0)
  return number > 0 ? `${number.toFixed(2)}%` : '未识别'
}

function reasonText(value) {
  const map = {
    natural_wear: '自然损耗',
    unproven: '无法证明原因',
    tenant_fault: '承租人过错',
  }
  return map[value] || '未识别'
}

function propertyDefectText(facts) {
  if (facts.serious_defect) return '严重'
  if (facts.general_defect) return '一般'
  if (facts.minor_defect) return '轻微'
  return '未识别'
}

function workDefectText(facts) {
  if (facts.worthless_defect) return '完全无价值'
  if (facts.serious_defect) return '严重'
  if (facts.minor_defect) return '轻微'
  return '未识别'
}

function agencyScopeText(facts) {
  if (facts.special_mandate) return '特别委托'
  if (facts.general_mandate) return '概括委托'
  return '未识别'
}

function fillExample() {
  caseText.value = exampleTexts[contractType.value]
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
