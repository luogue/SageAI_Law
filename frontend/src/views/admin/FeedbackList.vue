<template>
  <div class="feedback-list">
    <!-- 筛选栏 -->
    <el-card class="filter-card">
      <div class="filter-row">
        <el-select v-model="filters.status" placeholder="审核状态" clearable>
          <el-option label="全部" value="" />
          <el-option label="待审核" value="pending" />
          <el-option label="已通过" value="approved" />
          <el-option label="已驳回" value="rejected" />
        </el-select>
        
        <el-select v-model="filters.feedback_type" placeholder="反馈类型" clearable>
          <el-option label="全部" value="" />
          <el-option label="有用" value="useful" />
          <el-option label="没用" value="not_useful" />
          <el-option label="详细反馈" value="detailed" />
        </el-select>
        
        <el-select v-model="filters.category" placeholder="分类标签" clearable>
          <el-option label="全部" value="" />
          <el-option label="风险遗漏" value="风险遗漏" />
          <el-option label="误判" value="误判" />
          <el-option label="建议不实用" value="建议不实用" />
          <el-option label="其他" value="其他" />
        </el-select>
        
        <el-button type="primary" @click="loadFeedbacks">查询</el-button>
      </div>
    </el-card>
    
    <!-- 表格区域 -->
    <el-card>
      <div class="table-header">
        <span>共 {{ total }} 条记录</span>
        <div v-if="selectedIds.length > 0" class="batch-actions">
          <span>已选择 {{ selectedIds.length }} 条</span>
          <el-button size="small" type="primary" @click="handleBatchApprove">批量通过</el-button>
          <el-button size="small" type="danger" @click="handleBatchReject">批量驳回</el-button>
        </div>
      </div>
      
      <el-table 
        :data="feedbacks" 
        border 
        :selectable="row => row.status === 'pending'"
        @selection-change="handleSelectionChange"
      >
        <el-table-column type="selection" width="55" />
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="mobile" label="手机号" width="120" />
        <el-table-column 
          prop="feedback_type" 
          label="反馈类型" 
          width="100"
          :formatter="formatFeedbackType"
        />
        <el-table-column 
          prop="categories" 
          label="分类标签" 
          width="150"
          :formatter="formatCategories"
        />
        <el-table-column 
          prop="comment" 
          label="描述内容" 
          :formatter="formatComment"
        />
        <el-table-column 
          prop="upload_consent" 
          label="是否上传合同" 
          width="120"
          :formatter="formatUploadConsent"
        />
        <el-table-column 
          prop="status" 
          label="审核状态" 
          width="100"
          :formatter="formatStatus"
        />
        <el-table-column 
          prop="bonus_awarded" 
          label="奖励发放" 
          width="100"
          :formatter="formatBonus"
        />
        <el-table-column prop="created_at" label="提交时间" width="160" />
        <el-table-column label="操作" width="200">
          <template #default="scope">
            <el-button size="small" @click="handleViewDetail(scope.row)">查看详情</el-button>
            <el-button 
              v-if="scope.row.status === 'pending'" 
              size="small" 
              type="primary" 
              @click="handleApprove(scope.row)"
            >
              通过
            </el-button>
            <el-button 
              v-if="scope.row.status === 'pending'" 
              size="small" 
              type="danger" 
              @click="handleReject(scope.row)"
            >
              驳回
            </el-button>
          </template>
        </el-table-column>
      </el-table>
      
      <el-pagination
        @size-change="handleSizeChange"
        @current-change="handlePageChange"
        :current-page="page"
        :page-sizes="[10, 20, 50, 100]"
        :page-size="size"
        layout="total, sizes, prev, pager, next, jumper"
        :total="total"
      >
      </el-pagination>
    </el-card>
    
    <!-- 详情弹窗 -->
    <el-dialog title="反馈详情" :visible.sync="detailVisible" width="600px">
      <div v-if="currentFeedback" class="detail-content">
        <div class="detail-row">
          <span class="label">手机号：</span>
          <span>{{ currentFeedback.mobile }}</span>
        </div>
        <div class="detail-row">
          <span class="label">反馈类型：</span>
          <span>{{ formatFeedbackType(currentFeedback) }}</span>
        </div>
        <div class="detail-row">
          <span class="label">分类标签：</span>
          <span>{{ currentFeedback.categories?.join(', ') || '无' }}</span>
        </div>
        <div class="detail-row">
          <span class="label">描述内容：</span>
          <span>{{ currentFeedback.comment }}</span>
        </div>
        <div class="detail-row">
          <span class="label">是否上传合同：</span>
          <span>{{ currentFeedback.upload_consent ? '是' : '否' }}</span>
        </div>
        <div v-if="currentFeedback.contract_text" class="detail-row">
          <span class="label">合同原文：</span>
          <pre class="contract-text">{{ currentFeedback.contract_text }}</pre>
        </div>
        <div class="detail-row">
          <span class="label">审核状态：</span>
          <span>{{ formatStatus(currentFeedback) }}</span>
        </div>
        <div class="detail-row">
          <span class="label">奖励额度：</span>
          <span>{{ currentFeedback.bonus_awarded }} 次</span>
        </div>
        <div v-if="currentFeedback.reject_reason" class="detail-row">
          <span class="label">驳回原因：</span>
          <span>{{ currentFeedback.reject_reason }}</span>
        </div>
        <div class="detail-row">
          <span class="label">提交时间：</span>
          <span>{{ currentFeedback.created_at }}</span>
        </div>
      </div>
    </el-dialog>
    
    <!-- 通过审核弹窗 -->
    <el-dialog title="通过审核" :visible.sync="approveVisible">
      <el-form :model="approveForm">
        <el-form-item label="奖励额度">
          <el-input-number 
            v-model="approveForm.bonusCredits" 
            :min="1" 
            :max="10" 
            :step="1"
          />
          <span class="unit">次免费审查额度</span>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="approveVisible = false">取消</el-button>
        <el-button type="primary" @click="confirmApprove">确认通过</el-button>
      </template>
    </el-dialog>
    
    <!-- 驳回审核弹窗 -->
    <el-dialog title="驳回审核" :visible.sync="rejectVisible">
      <el-form :model="rejectForm">
        <el-form-item label="驳回原因（选填）">
          <el-input 
            v-model="rejectForm.reason" 
            type="textarea" 
            :rows="3" 
            placeholder="请输入驳回原因..."
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="rejectVisible = false">取消</el-button>
        <el-button type="danger" @click="confirmReject">确认驳回</el-button>
      </template>
    </el-dialog>
    
    <!-- 批量通过弹窗 -->
    <el-dialog title="批量通过审核" :visible.sync="batchApproveVisible">
      <el-form :model="batchApproveForm">
        <el-form-item label="奖励额度（每条）">
          <el-input-number 
            v-model="batchApproveForm.bonusCredits" 
            :min="1" 
            :max="10" 
            :step="1"
          />
          <span class="unit">次免费审查额度</span>
        </el-form-item>
        <p class="batch-count">将为 {{ selectedIds.length }} 条反馈发放奖励</p>
      </el-form>
      <template #footer>
        <el-button @click="batchApproveVisible = false">取消</el-button>
        <el-button type="primary" @click="confirmBatchApprove">确认批量通过</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { 
  getFeedbacks, 
  getFeedbackDetail, 
  approveFeedback, 
  rejectFeedback, 
  batchApproveFeedbacks 
} from '../../api/admin'

const feedbacks = ref([])
const total = ref(0)
const page = ref(1)
const size = ref(20)
const selectedIds = ref([])

const filters = reactive({
  status: '',
  feedback_type: '',
  category: ''
})

const detailVisible = ref(false)
const approveVisible = ref(false)
const rejectVisible = ref(false)
const batchApproveVisible = ref(false)

const currentFeedback = ref(null)
const currentId = ref(null)

const approveForm = reactive({ bonusCredits: 3 })
const rejectForm = reactive({ reason: '' })
const batchApproveForm = reactive({ bonusCredits: 3 })

async function loadFeedbacks() {
  try {
    const params = {
      page: page.value,
      size: size.value
    }
    if (filters.status) params.status = filters.status
    if (filters.feedback_type) params.feedback_type = filters.feedback_type
    if (filters.category) params.category = filters.category
    
    const result = await getFeedbacks(params)
    feedbacks.value = result.data
    total.value = result.total
  } catch (e) {
    console.error('加载反馈列表失败:', e)
  }
}

function handleSizeChange(val) {
  size.value = val
  loadFeedbacks()
}

function handlePageChange(val) {
  page.value = val
  loadFeedbacks()
}

function handleSelectionChange(val) {
  selectedIds.value = val.map(item => item.id)
}

async function handleViewDetail(row) {
  try {
    const result = await getFeedbackDetail(row.id)
    currentFeedback.value = result.data
    detailVisible.value = true
  } catch (e) {
    console.error('获取反馈详情失败:', e)
  }
}

function handleApprove(row) {
  currentId.value = row.id
  approveForm.bonusCredits = 3
  approveVisible.value = true
}

function handleReject(row) {
  currentId.value = row.id
  rejectForm.reason = ''
  rejectVisible.value = true
}

async function confirmApprove() {
  try {
    await approveFeedback(currentId.value, approveForm.bonusCredits)
    approveVisible.value = false
    loadFeedbacks()
  } catch (e) {
    console.error('审核通过失败:', e)
  }
}

async function confirmReject() {
  try {
    await rejectFeedback(currentId.value, rejectForm.reason)
    rejectVisible.value = false
    loadFeedbacks()
  } catch (e) {
    console.error('驳回审核失败:', e)
  }
}

function handleBatchApprove() {
  batchApproveForm.bonusCredits = 3
  batchApproveVisible.value = true
}

async function confirmBatchApprove() {
  try {
    await batchApproveFeedbacks(selectedIds.value, batchApproveForm.bonusCredits)
    batchApproveVisible.value = false
    selectedIds.value = []
    loadFeedbacks()
  } catch (e) {
    console.error('批量审核失败:', e)
  }
}

function handleBatchReject() {
  // 批量驳回（简单处理：不填写原因）
  selectedIds.value.forEach(id => {
    rejectFeedback(id, '')
  })
  selectedIds.value = []
  loadFeedbacks()
}

// 格式化函数
function formatFeedbackType(row) {
  const types = {
    'useful': '有用',
    'not_useful': '没用',
    'detailed': '详细反馈'
  }
  return types[row.feedback_type] || row.feedback_type
}

function formatCategories(row) {
  const cats = row.categories
  if (!cats) return '无'
  return Array.isArray(cats) ? cats.join(', ') : cats
}

function formatComment(row) {
  const comment = row.comment
  if (!comment) return '无'
  return comment.length > 50 ? comment.slice(0, 50) + '...' : comment
}

function formatUploadConsent(row) {
  return row.upload_consent ? '是' : '否'
}

function formatStatus(row) {
  const status = {
    'pending': '待审核',
    'approved': '已通过',
    'rejected': '已驳回'
  }
  return status[row.status] || row.status
}

function formatBonus(row) {
  return row.bonus_awarded > 0 ? `${row.bonus_awarded} 次` : '未发放'
}

onMounted(() => {
  loadFeedbacks()
})
</script>

<style scoped>
.feedback-list {
  padding: 20px;
}

.filter-card {
  margin-bottom: 16px;
}

.filter-row {
  display: flex;
  gap: 16px;
  align-items: center;
}

.filter-row .el-select {
  width: 160px;
}

.table-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.batch-actions {
  display: flex;
  align-items: center;
  gap: 12px;
}

.detail-content {
  padding: 10px 0;
}

.detail-row {
  margin-bottom: 12px;
  display: flex;
}

.detail-row .label {
  width: 100px;
  font-weight: bold;
  color: #606266;
}

.contract-text {
  flex: 1;
  background: #f5f5f5;
  padding: 10px;
  border-radius: 4px;
  max-height: 200px;
  overflow-y: auto;
  white-space: pre-wrap;
}

.unit {
  margin-left: 8px;
  color: #909399;
}

.batch-count {
  color: #909399;
  margin-top: 8px;
}
</style>
