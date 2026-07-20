<template>
  <div class="user-list-container">
    <div class="page-header">
      <h2>用户管理</h2>
      <el-button type="primary" @click="showCreateDialog = true">
        <el-icon><Plus /></el-icon>
        创建用户
      </el-button>
    </div>

    <!-- 筛选栏 -->
    <el-card class="filter-card" shadow="never">
      <el-form :inline="true" :model="filters" size="default">
        <el-form-item label="手机号">
          <el-input v-model="filters.mobile" placeholder="搜索手机号" clearable />
        </el-form-item>
        <el-form-item label="状态">
          <el-select v-model="filters.status" placeholder="全部" clearable style="width: 120px;">
            <el-option label="审核中" value="pending" />
            <el-option label="正常" value="normal" />
            <el-option label="封禁" value="blocked" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">搜索</el-button>
          <el-button @click="handleReset">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <!-- 用户列表 -->
    <el-card class="list-card" shadow="never">
      <el-table :data="users" v-loading="loading" stripe style="width: 100%">
        <el-table-column prop="id" label="ID" width="60" />
        <el-table-column prop="mobile" label="手机号" width="140" />
        <el-table-column prop="bonus_credits" label="剩余额度" width="100" />
        <el-table-column label="状态" width="100">
          <template #default="{ row }">
            <el-tag v-if="row.status === 'normal'" type="success">正常</el-tag>
            <el-tag v-else-if="row.status === 'pending'" type="warning">审核中</el-tag>
            <el-tag v-else-if="row.status === 'blocked'" type="danger">封禁</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="注册时间" width="170">
          <template #default="{ row }">
            {{ formatDate(row.created_at) }}
          </template>
        </el-table-column>
        <el-table-column label="操作" min-width="260" fixed="right">
          <template #default="{ row }">
            <el-button size="small" @click="viewDetail(row)" :icon="View">详情</el-button>
            <el-button
              v-if="row.status === 'pending'"
              size="small"
              type="success"
              @click="handleApprove(row)"
              :loading="approvingId === row.id"
            >
              审核通过
            </el-button>
            <el-button
              v-if="row.status === 'normal'"
              size="small"
              type="warning"
              @click="showBanDialog(row)"
            >
              封禁
            </el-button>
            <el-button
              v-if="row.status === 'blocked'"
              size="small"
              type="primary"
              @click="handleUnban(row)"
            >
              解封
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页 -->
      <div class="pagination">
        <el-pagination
          v-model:current-page="pagination.page"
          :page-size="pagination.size"
          :total="pagination.total"
          layout="total, prev, pager, next"
          @current-change="loadUsers"
        />
      </div>
    </el-card>

    <!-- 创建用户对话框 -->
    <el-dialog v-model="showCreateDialog" title="创建新用户" width="460px" :close-on-click-modal="false">
      <el-form ref="createFormRef" :model="createForm" :rules="createRules" label-width="80px">
        <el-form-item label="手机号" prop="mobile">
          <el-input v-model="createForm.mobile" placeholder="请输入手机号" maxlength="11" />
        </el-form-item>
        <el-form-item label="密码" prop="password">
          <el-input v-model="createForm.password" type="password" placeholder="请输入密码" show-password />
        </el-form-item>
        <el-form-item label="赠送额度" prop="bonusCredits">
          <el-input-number v-model="createForm.bonusCredits" :min="0" :max="100" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showCreateDialog = false">取消</el-button>
        <el-button type="primary" @click="handleCreate" :loading="creating">确认创建</el-button>
      </template>
    </el-dialog>

    <!-- 封禁对话框 -->
    <el-dialog v-model="showBanDialogVisible" title="封禁用户" width="400px">
      <el-form label-width="80px">
        <el-form-item label="封禁原因">
          <el-input v-model="banReason" type="textarea" :rows="2" placeholder="可选" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showBanDialogVisible = false">取消</el-button>
        <el-button type="danger" @click="handleBan">确认封禁</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus, View } from '@element-plus/icons-vue'
import { getUsers, createUser, approveUser, banUser, unbanUser } from '@/api/admin'

const router = useRouter()

// 筛选
const filters = reactive({
  mobile: '',
  status: ''
})

// 列表
const users = ref([])
const loading = ref(false)
const pagination = reactive({
  page: 1,
  size: 20,
  total: 0
})

// 创建用户
const showCreateDialog = ref(false)
const creating = ref(false)
const createFormRef = ref(null)
const createForm = reactive({
  mobile: '',
  password: '',
  bonusCredits: 3
})
const createRules = {
  mobile: [
    { required: true, message: '请输入手机号', trigger: 'blur' },
    { pattern: /^1\d{10}$/, message: '手机号格式不正确', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码至少6位', trigger: 'blur' }
  ]
}

// 封禁
const showBanDialogVisible = ref(false)
const banTarget = ref(null)
const banReason = ref('')

// 审核中
const approvingId = ref(null)

// 加载用户列表
async function loadUsers() {
  loading.value = true
  try {
    const data = await getUsers({
      page: pagination.page,
      size: pagination.size,
      mobile: filters.mobile || undefined,
      status: filters.status || undefined
    })
    users.value = data.users || []
    pagination.total = data.total || 0
  } catch (err) {
    ElMessage.error(err.message || '加载失败')
  } finally {
    loading.value = false
  }
}

function handleSearch() {
  pagination.page = 1
  loadUsers()
}

function handleReset() {
  filters.mobile = ''
  filters.status = ''
  pagination.page = 1
  loadUsers()
}

// 创建用户
async function handleCreate() {
  const valid = await createFormRef.value?.validate().catch(() => false)
  if (!valid) return

  creating.value = true
  try {
    await createUser({
      mobile: createForm.mobile,
      password: createForm.password,
      bonusCredits: createForm.bonusCredits
    })
    ElMessage.success('用户创建成功')
    showCreateDialog.value = false
    createForm.mobile = ''
    createForm.password = ''
    createForm.bonusCredits = 3
    loadUsers()
  } catch (err) {
    ElMessage.error(err.message || '创建失败')
  } finally {
    creating.value = false
  }
}

// 审核通过
async function handleApprove(user) {
  try {
    await ElMessageBox.confirm(`确认审核通过用户 ${user.mobile}？`, '审核确认', {
      type: 'info'
    })
  } catch {
    return
  }

  approvingId.value = user.id
  try {
    await approveUser(user.id)
    ElMessage.success('审核通过')
    loadUsers()
  } catch (err) {
    ElMessage.error(err.message || '操作失败')
  } finally {
    approvingId.value = null
  }
}

// 封禁
function showBanDialog(user) {
  banTarget.value = user
  banReason.value = ''
  showBanDialogVisible.value = true
}

async function handleBan() {
  try {
    await banUser(banTarget.value.id, banReason.value)
    ElMessage.success('已封禁')
    showBanDialogVisible.value = false
    loadUsers()
  } catch (err) {
    ElMessage.error(err.message || '封禁失败')
  }
}

// 解封
async function handleUnban(user) {
  try {
    await unbanUser(user.id)
    ElMessage.success('已解封')
    loadUsers()
  } catch (err) {
    ElMessage.error(err.message || '解封失败')
  }
}

// 查看详情
function viewDetail(user) {
  router.push(`/admin/users/${user.id}`)
}

function formatDate(dateStr) {
  if (!dateStr) return '-'
  return new Date(dateStr).toLocaleString('zh-CN')
}

onMounted(() => {
  loadUsers()
})
</script>

<style scoped>
.user-list-container {
  padding: 20px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.page-header h2 {
  margin: 0;
  font-size: 20px;
}

.filter-card {
  margin-bottom: 16px;
}

.pagination {
  margin-top: 16px;
  display: flex;
  justify-content: flex-end;
}
</style>
