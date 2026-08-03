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
  guarantee: '保证合同只写担保人签字，未约定保证方式。债权人要求保证人直接承担责任，保证人主张先诉抗辩权。',
  finance_lease: '融资租赁合同中承租人欠付租金，经出租人催告后仍未支付，出租人同时请求支付全部租金并解除合同收回租赁物。',
  warehouse: '仓储物在储存期内毁损灭失，保管人主张系包装不符合约定造成，存货人要求保管人赔偿货值30000元。',
  construction: '建设工程施工合同无效，但工程竣工验收合格，承包人请求参照合同约定折价补偿工程价款100万元。',
  technology: '委托开发完成发明创造，双方未约定专利申请权归属，委托人要求确认自己享有专利申请权。',
  commission_agency: '行纪人以自己名义为委托人出售货物，低于委托人指定价格卖出，未经委托人同意，但愿意补偿差额。',
  utility_supply: '供电公司因用户拖欠电费中止供电，但未催告、未给予合理期限，用户要求恢复供电并赔偿损失3000元。',
  gift: '赠与人承诺赠与房屋但尚未办理过户，赠与合同未公证，赠与人反悔要求撤销赠与。',
  brokerage: '委托人接受中介带看和房源信息后，绕开中介直接与卖方签订买卖合同，中介要求支付中介费。',
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
  { label: '保证合同', value: 'guarantee' },
  { label: '融资租赁', value: 'finance_lease' },
  { label: '仓储合同', value: 'warehouse' },
  { label: '建设工程', value: 'construction' },
  { label: '技术合同', value: 'technology' },
  { label: '行纪合同', value: 'commission_agency' },
  { label: '供用电/水/气/热力', value: 'utility_supply' },
  { label: '赠与合同', value: 'gift' },
  { label: '中介合同', value: 'brokerage' },
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
    guarantee: '请输入案件事实。例如：保证方式是否明确、保证期间是否已过、债权人是否在期间内行权、一般保证能否先诉抗辩、主合同变更是否经保证人同意。',
    finance_lease: '请输入案件事实。例如：租赁物是否真实、是否售后回租、承租人是否欠租、出租人选择全部租金还是解除收回、租赁物瑕疵或毁损灭失由谁负责。',
    warehouse: '请输入案件事实。例如：是否构成商事仓储、仓单是否转让或质押、入库验收是否通知、仓储物毁损灭失原因、是否逾期提取或欠付仓储费。',
    construction: '请输入案件事实。例如：资质、招投标、规划许可是否影响合同效力；工程是否验收合格；工程款、优先受偿权、实际施工人、工期、质量或解除争议。',
    technology: '请输入案件事实。例如：技术开发、转让、许可、咨询或服务类型；技术成果权属；非法垄断、侵害技术秘密、开发失败、后续改进或咨询决策风险。',
    commission_agency: '请输入案件事实。例如：行纪人是否以自己名义交易、是否违反价格指示、第三人是否违约、委托物是否毁损或变质、报酬是否支付、是否留置或提存。',
    utility_supply: '请输入案件事实。例如：供用电/水/气/热力类型、是否拒绝签约、供应是否中断或质量不达标、欠费停供是否催告、计量是否有误、设施维护责任在哪一侧。',
    gift: '请输入案件事实。例如：是否无偿给予并接受、财产权利是否已交付或登记、赠与是否公证/公益/附义务、赠与人是否撤销、撤销是否超过期限、是否存在瑕疵或穷困抗辩。',
    brokerage: '请输入案件事实。例如：是否存在中介服务、是否促成合同成立、是否跳单、报酬如何约定、是否隐瞒重要事实、是否解除或主张必要费用。',
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
    ['保证合同关系', boolText(facts.guarantee_contract)],
    ['主合同无效', boolText(facts.main_contract_invalid)],
    ['保证合同无效', boolText(facts.guarantee_invalid)],
    ['特殊保证人主体', boolText(Boolean(facts.state_org_guarantor || facts.public_nonprofit_guarantor))],
    ['公司对外担保', boolText(facts.company_guarantor)],
    ['公司决议/善意', boolText(Boolean(facts.company_resolution || facts.creditor_good_faith))],
    ['保证方式不明', boolText(facts.unclear_guarantee_type)],
    ['一般保证', boolText(facts.general_guarantee)],
    ['连带保证', boolText(facts.joint_guarantee_type)],
    ['保证期间约定不明', boolText(facts.guarantee_period_unclear)],
    ['保证期间已过', boolText(facts.period_expired)],
    ['期间内向债务人行权', boolText(facts.action_against_debtor)],
    ['期间内向保证人行权', boolText(facts.action_against_guarantor)],
    ['仅起诉一般保证人', boolText(facts.only_sue_general_guarantor)],
    ['放弃先诉抗辩', boolText(facts.waived_prior_lawsuit)],
    ['主合同变更', boolText(facts.main_contract_changed)],
    ['债权转让', boolText(facts.credit_assignment)],
    ['债务转移', boolText(facts.debt_transfer)],
    ['共同保证', boolText(facts.multiple_guarantors)],
    ['最高额保证', boolText(facts.maximum_guarantee)],
    ['保证人已代偿', boolText(facts.guarantor_paid)],
    ['代偿金额', moneyText(facts.paid_amount)],
    ['届满后签字', boolText(facts.post_period_signature)],
    ['主债务时效届满', boolText(facts.main_debt_limitation_expired)],
    ['融资租赁合同关系', boolText(facts.finance_lease_contract)],
    ['融资租赁定性争议', boolText(facts.nature_dispute)],
    ['售后回租', boolText(facts.sale_leaseback)],
    ['虚构租赁物', boolText(facts.fake_asset)],
    ['行政许可争议', boolText(facts.admin_license_issue)],
    ['融资租赁合同无效', boolText(facts.contract_invalid)],
    ['出卖人未交付', boolText(facts.seller_non_delivery)],
    ['承租人拒收', boolText(facts.lessee_refuses_accept)],
    ['租赁物质量瑕疵', boolText(facts.quality_defect)],
    ['承租人自行选择租赁物', boolText(facts.lessee_selected_asset)],
    ['出租人干预选择', boolText(facts.lessor_intervened_choice)],
    ['依赖出租人技能', boolText(facts.lessor_skill_reliance)],
    ['出租人未协助索赔', boolText(facts.lessor_failed_assist)],
    ['出租人擅自收回', boolText(facts.lessor_wrongfully_repossess)],
    ['融资租赁欠租', boolText(facts.unpaid_rent)],
    ['出租人已催告', boolText(facts.lessor_urged)],
    ['请求全部租金', boolText(facts.request_all_rent)],
    ['解除并收回租赁物', boolText(facts.request_terminate_repossess)],
    ['同时主张两项救济', boolText(facts.request_both_remedies)],
    ['租赁物毁损灭失', boolText(facts.asset_loss)],
    ['承租人过错毁损', boolText(facts.lessee_fault_loss)],
    ['租赁物擅自处分', boolText(facts.unauthorized_disposition)],
    ['所有权已登记', boolText(facts.ownership_registered)],
    ['所有权未登记', boolText(facts.ownership_unregistered)],
    ['期满归承租人', boolText(facts.end_ownership_agreed)],
    ['象征性价款', boolText(facts.symbolic_price)],
    ['已付大部分租金', boolText(facts.paid_most_rent)],
    ['租赁物价值', moneyText(facts.asset_value)],
    ['欠付租金及费用', moneyText(facts.unpaid_fees)],
    ['买卖合同障碍', boolText(facts.sale_contract_invalid)],
    ['回购担保', boolText(facts.repurchase_guarantee)],
    ['合同权利转让', boolText(facts.contract_assignment)],
    ['仓储合同关系', boolText(facts.warehouse_contract)],
    ['仓储/保管定性争议', boolText(facts.nature_dispute)],
    ['仓储营业主体', boolText(facts.warehouse_business)],
    ['一般保管关系', boolText(facts.general_safekeeping)],
    ['仓储资质争议', boolText(facts.qualification_issue)],
    ['仓储物已入库', boolText(facts.goods_delivered)],
    ['仓单/入库单', boolText(facts.receipt_issued)],
    ['仓单转让', boolText(facts.receipt_transfer)],
    ['仓单质押', boolText(facts.receipt_pledge)],
    ['仓单背书', boolText(facts.receipt_endorsed)],
    ['保管人签章', boolText(facts.keeper_signed_receipt)],
    ['多人主张提货', boolText(facts.multiple_claimants)],
    ['合法仓单持有人', boolText(facts.receipt_holder)],
    ['入库验收争议', boolText(facts.acceptance_dispute)],
    ['仓储物不符约定', boolText(facts.goods_nonconform)],
    ['及时通知', boolText(facts.timely_notice)],
    ['未及时通知', boolText(facts.no_timely_notice)],
    ['危险/易变质物品', boolText(facts.dangerous_goods)],
    ['危险性质已说明', boolText(facts.hazard_explained)],
    ['仓储物毁损灭失', boolText(facts.damage_or_loss)],
    ['储存期内', boolText(facts.in_storage_period)],
    ['保管不善', boolText(facts.improper_custody)],
    ['自然性质免责', boolText(facts.natural_property)],
    ['包装不符免责', boolText(facts.bad_packaging)],
    ['超期储存免责', boolText(facts.expired_storage)],
    ['部分毁损灭失', boolText(facts.partial_damage)],
    ['价值减损', boolText(facts.value_depreciation)],
    ['仓储损失金额', moneyText(facts.actual_loss)],
    ['检查/取样请求', boolText(facts.inspection_request)],
    ['发现变质损坏', boolText(facts.deterioration_found)],
    ['损失扩大', boolText(facts.loss_expanded)],
    ['危及其他仓储物', boolText(facts.danger_to_others)],
    ['紧急处置', boolText(Boolean(facts.emergency || facts.disposed))],
    ['提前提取', boolText(facts.early_retrieval)],
    ['逾期提取', boolText(facts.overdue_retrieval)],
    ['储存期限不明', boolText(facts.unclear_storage_period)],
    ['欠付仓储费', boolText(facts.unpaid_storage_fee)],
    ['仓储留置权', boolText(facts.lien_claim)],
    ['仓储费金额', moneyText(facts.fee_amount)],
    ['仓储合同解除', boolText(facts.termination_request)],
    ['存货人转让', boolText(facts.depositor_assignment)],
    ['建设工程合同关系', boolText(facts.construction_contract)],
    ['勘察合同', boolText(facts.survey_contract)],
    ['设计合同', boolText(facts.design_contract)],
    ['施工合同', boolText(facts.construction_work_contract)],
    ['建设工程合同无效', boolText(facts.contract_invalid)],
    ['资质缺陷', boolText(facts.qualification_defect)],
    ['竣工前取得资质', boolText(facts.qualification_before_completion)],
    ['挂靠/借用资质', boolText(facts.affiliation)],
    ['招投标违法', boolText(facts.tender_illegal)],
    ['规划许可缺失', boolText(facts.planning_missing)],
    ['违法分包/转包', boolText(facts.illegal_subcontract)],
    ['黑白合同', boolText(facts.black_white_contract)],
    ['实质性内容不一致', boolText(facts.substantive_inconsistency)],
    ['劳务分包', boolText(facts.labor_subcontract)],
    ['工程验收合格', boolText(facts.project_accepted)],
    ['工程验收不合格', boolText(facts.project_unaccepted)],
    ['工程价款', moneyText(facts.project_price)],
    ['修复费用', moneyText(facts.repair_cost)],
    ['工期争议', boolText(facts.period_dispute)],
    ['开工通知', boolText(facts.start_notice)],
    ['实际进场', boolText(facts.actual_entry)],
    ['发包人拖延验收', boolText(facts.delay_acceptance)],
    ['发包人擅自使用', boolText(facts.unauthorized_use)],
    ['工程质量瑕疵', boolText(facts.quality_defect)],
    ['质保金返还', boolText(facts.quality_deposit_return)],
    ['质保金金额', moneyText(facts.quality_deposit_amount)],
    ['隐蔽工程', boolText(facts.hidden_work)],
    ['欠付工程款', boolText(facts.unpaid_project_price)],
    ['工程价款优先受偿', boolText(facts.priority_claim)],
    ['18个月内行使', boolText(facts.within_18_months)],
    ['超过18个月', boolText(facts.beyond_18_months)],
    ['实际施工人', boolText(facts.actual_constructor)],
    ['发包人欠付范围', moneyText(facts.amount_owed_by_employer)],
    ['建设工程合同解除', boolText(facts.termination_request)],
    ['停工窝工损失', boolText(Boolean(facts.stoppage_loss || facts.employer_material_delay))],
    ['建设工程损失金额', moneyText(facts.actual_loss)],
    ['工程款利息', boolText(facts.interest_claim)],
    ['利息金额', moneyText(facts.interest_amount)],
    ['技术合同关系', boolText(facts.technology_contract)],
    ['技术合同类型争议', boolText(facts.nature_dispute)],
    ['技术开发合同', boolText(facts.development_contract)],
    ['委托开发', boolText(facts.commissioned_development)],
    ['合作开发', boolText(facts.cooperative_development)],
    ['技术转让合同', boolText(facts.transfer_contract)],
    ['技术许可合同', boolText(facts.license_contract)],
    ['技术咨询合同', boolText(facts.consulting_contract)],
    ['技术服务合同', boolText(facts.service_contract)],
    ['非法垄断技术', boolText(facts.illegal_monopoly)],
    ['侵害技术成果', boolText(facts.infringe_achievement)],
    ['善意取得技术秘密', boolText(facts.good_faith_acquirer)],
    ['合理使用费', moneyText(facts.reasonable_use_fee)],
    ['欺诈订立技术合同', boolText(facts.fraud_contract)],
    ['职务技术成果', boolText(facts.duty_achievement)],
    ['非职务技术成果', boolText(facts.non_duty_achievement)],
    ['技术成果权属争议', boolText(facts.ownership_dispute)],
    ['技术合同解除', boolText(facts.termination_request)],
    ['催告后超过30日', boolText(facts.over_30_days)],
    ['技术进出口', boolText(facts.technology_import_export)],
    ['开发失败', boolText(facts.development_failed)],
    ['风险分担约定', boolText(facts.risk_agreed)],
    ['发明创造/专利申请权', boolText(facts.invention_creation)],
    ['技术秘密成果', boolText(facts.technical_secret_result)],
    ['许可人无权/技术瑕疵', boolText(Boolean(facts.licensor_not_owner || facts.technology_defective))],
    ['未支付使用费', boolText(facts.fee_unpaid)],
    ['许可超范围', boolText(Boolean(facts.license_over_scope || facts.licensee_over_scope))],
    ['许可实施侵权', boolText(Boolean(facts.licensee_as_agreed && facts.third_party_infringement))],
    ['后续改进成果', boolText(facts.followup_improvement)],
    ['咨询决策损失', boolText(facts.decision_loss)],
    ['咨询报告符合要求', boolText(facts.consulting_report_conform)],
    ['新技术成果', boolText(facts.new_result)],
    ['科研组织无主体资格', boolText(facts.research_org_no_capacity)],
    ['行纪合同关系', boolText(facts.commission_agency_contract)],
    ['行纪合同性质争议', boolText(facts.nature_dispute)],
    ['以自己名义交易', boolText(facts.own_name_trade)],
    ['以委托人名义', boolText(facts.principal_name)],
    ['中介服务', boolText(facts.intermediary_service)],
    ['贸易活动', boolText(facts.trade_activity)],
    ['口头行纪合同', boolText(facts.oral_contract)],
    ['行纪关系证据', boolText(facts.evidence_exists)],
    ['行纪人身份混同', boolText(facts.identity_confusion)],
    ['委托物毁损灭失', boolText(facts.custody_damage)],
    ['保管不善', boolText(facts.improper_custody)],
    ['费用负担争议', boolText(facts.expense_claim)],
    ['第三人交易合同', boolText(facts.third_party_contract)],
    ['第三人违约', boolText(facts.third_party_default)],
    ['恶意串通', boolText(facts.malicious_collusion)],
    ['价格指示', boolText(facts.price_instruction)],
    ['低卖/高买', boolText(Boolean(facts.low_sell || facts.high_buy))],
    ['高卖/低买', boolText(Boolean(facts.high_sell || facts.low_buy))],
    ['委托人同意', boolText(facts.principal_consent)],
    ['补偿差额', boolText(facts.difference_compensated)],
    ['市场定价商品', boolText(facts.market_priced_goods)],
    ['介入权主张', boolText(facts.intervention_claim)],
    ['委托物瑕疵/易变质', boolText(facts.defective_or_perishable)],
    ['处分委托物', boolText(facts.disposal_claim)],
    ['提存主张', boolText(facts.deposit_claim)],
    ['报酬请求', boolText(facts.remuneration_claim)],
    ['逾期未付报酬', boolText(facts.remuneration_unpaid)],
    ['委托事务完成', boolText(facts.matter_completed)],
    ['留置权主张', boolText(facts.lien_claim)],
    ['转委托', boolText(facts.sub_entrustment)],
    ['解除行纪合同', boolText(facts.termination_request)],
    ['行纪损失金额', moneyText(facts.actual_loss)],
    ['供用合同关系', boolText(facts.utility_supply_contract)],
    ['供用电合同', boolText(facts.electricity_contract)],
    ['供用水合同', boolText(facts.water_contract)],
    ['供用气合同', boolText(facts.gas_contract)],
    ['供用热力合同', boolText(facts.heat_contract)],
    ['合同类型争议', boolText(facts.contract_type_dispute)],
    ['未签书面供用合同', boolText(facts.no_written_contract)],
    ['实际供应', boolText(facts.actual_supply)],
    ['用户实际使用', boolText(facts.user_used)],
    ['已支付费用', boolText(facts.paid_fee)],
    ['拒绝订立合同', boolText(facts.refuse_contract)],
    ['合理签约要求', boolText(facts.reasonable_request)],
    ['供应质量争议', boolText(facts.supply_quality_dispute)],
    ['供应质量不达标', boolText(facts.supply_quality_nonconform)],
    ['供应中断', boolText(facts.supply_interruption)],
    ['检修/限供中断', boolText(Boolean(facts.maintenance_interruption || facts.legal_power_limit))],
    ['事先通知', boolText(facts.prior_notice)],
    ['自然灾害', boolText(facts.natural_disaster)],
    ['及时抢修', boolText(facts.timely_repair)],
    ['用户欠费', boolText(facts.unpaid_fee)],
    ['已催告', boolText(facts.urged)],
    ['给予合理期限', boolText(facts.reasonable_period_given)],
    ['中止供应', boolText(facts.supply_suspended)],
    ['按国家程序中止', boolText(facts.statutory_procedure)],
    ['物业断水断电', boolText(facts.property_company_cutoff)],
    ['用户违规使用', boolText(facts.illegal_use)],
    ['违规转供', boolText(facts.sub_supply)],
    ['计量争议', boolText(facts.metering_dispute)],
    ['计量误差', boolText(facts.meter_error)],
    ['设施维护争议', boolText(facts.maintenance_dispute)],
    ['供应方侧设施', boolText(facts.boundary_supplier_side)],
    ['用户侧设施', boolText(facts.boundary_user_side)],
    ['供暖温度争议', boolText(facts.heating_temp_dispute)],
    ['供暖测温证据', boolText(facts.heating_evidence)],
    ['恢复供应承诺', boolText(facts.commitment_restore_time)],
    ['违反恢复承诺', boolText(facts.commitment_breached)],
    ['供用欠费金额', moneyText(facts.fee_amount)],
    ['供用违约金', moneyText(facts.liquidated_damage_amount)],
    ['赠与合同关系', boolText(facts.gift_contract)],
    ['赠与性质争议', boolText(facts.nature_dispute)],
    ['无偿给予意思', boolText(facts.gratuitous_intent)],
    ['受赠人接受', boolText(facts.donee_accepts)],
    ['存在对价', boolText(facts.consideration)],
    ['公证赠与', boolText(facts.notarized_gift)],
    ['公益/道德义务赠与', boolText(Boolean(facts.public_welfare_gift || facts.moral_obligation_gift))],
    ['附义务赠与', boolText(facts.obligation_attached)],
    ['需办理登记', boolText(facts.registration_required)],
    ['已办理登记', boolText(facts.registration_done)],
    ['权利已转移', boolText(facts.right_transferred)],
    ['任意撤销主张', boolText(facts.arbitrary_revocation_claim)],
    ['解除表述', boolText(facts.termination_word)],
    ['不得撤销约定', boolText(facts.waiver_revocation_agreement)],
    ['法定撤销主张', boolText(facts.statutory_revocation_claim)],
    ['严重侵害/不扶养/不履义务', boolText(Boolean(facts.serious_infringement || facts.support_duty_unfulfilled || facts.agreed_obligation_unfulfilled))],
    ['超过一年', boolText(facts.over_one_year)],
    ['继承人/法代撤销', boolText(facts.heir_or_agent_revocation)],
    ['超过六个月', boolText(facts.over_six_months)],
    ['请求交付赠与物', boolText(facts.delivery_claim)],
    ['赠与财产毁损灭失', boolText(facts.property_destroyed)],
    ['赠与财产瑕疵', boolText(facts.gift_property_defect)],
    ['故意不告知/保证无瑕疵', boolText(Boolean(facts.deliberate_non_disclosure || facts.guaranteed_no_defect))],
    ['穷困抗辩', boolText(facts.poverty_defense)],
    ['经济显著恶化', boolText(facts.economic_deteriorated)],
    ['严重影响生活经营', boolText(facts.serious_life_impact)],
    ['撤销后返还请求', boolText(facts.return_claim)],
    ['受赠人先死亡', boolText(facts.donee_predeceased)],
    ['赠与人死亡后履行请求', boolText(facts.donor_dead_inheritance_request)],
    ['赠与损失金额', moneyText(facts.actual_loss)],
    ['赠与财产价值', moneyText(facts.property_value)],
    ['中介合同关系', boolText(facts.brokerage_contract)],
    ['中介性质争议', boolText(facts.nature_dispute)],
    ['报告/媒介服务', boolText(Boolean(facts.intro_or_media_service || facts.report_brokerage || facts.media_brokerage))],
    ['不参与交易合同', boolText(facts.not_party_to_deal)],
    ['口头中介协议', boolText(facts.oral_contract)],
    ['存在中介证据', boolText(facts.evidence_exists)],
    ['格式条款争议', boolText(facts.standard_clause_dispute)],
    ['如实报告争议', boolText(facts.truthful_report_dispute)],
    ['隐瞒/虚假信息', boolText(Boolean(facts.important_fact_hidden || facts.false_information))],
    ['委托人损失', boolText(facts.principal_loss)],
    ['尽力义务争议', boolText(facts.best_efforts_dispute)],
    ['工作人员行为争议', boolText(facts.staff_act_dispute)],
    ['委托人信息有误', boolText(facts.principal_wrong_info)],
    ['跳单主张', boolText(facts.bypass_claim)],
    ['接受中介服务', boolText(facts.accepted_service)],
    ['利用交易机会', boolText(facts.used_opportunity)],
    ['绕开直接签约', boolText(facts.bypassed_direct_contract)],
    ['非独家/其他中介', boolText(Boolean(facts.non_exclusive_entrustment || facts.other_broker_legitimate))],
    ['促成合同成立', boolText(facts.contract_concluded)],
    ['交易未成', boolText(facts.contract_not_concluded)],
    ['中介报酬主张', boolText(facts.remuneration_claim)],
    ['必要费用主张', boolText(facts.necessary_expense_claim)],
    ['政策原因交易不成', boolText(facts.policy_failure)],
    ['解除中介合同', boolText(facts.termination_request)],
    ['后合同义务争议', boolText(facts.post_contract_obligation)],
    ['中介举证责任争议', boolText(facts.burden_proof_dispute)],
    ['中介金额', moneyText(facts.actual_loss)],
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
