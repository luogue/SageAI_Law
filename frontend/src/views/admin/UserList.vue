<template>
  <div class="user-list-page">
    <!-- 筛选栏 -->
    <div class="filter-bar">
      <div class="filter-item">
        <span class="filter-label">手机号搜索：</span>
        <el-input
          v-model="filterMobile"
          placeholder="输入手机号搜索"
          style="width: 250px"
          @keyup.enter="handleFilter"
        />
      </div>
      <div class="filter-item">
        <span class="filter-label">状态筛选：</span>
        <el-select
          v-model="filterStatus"
          placeholder="全部状态"
          clearable
          style="width: 150px"
          @change="handleFilter"
        >
          <el-option label="正常" value="normal" />
          <el-option label="封禁" value="blocked" />
        </el-select>
      </div>
      <div class="filter-item">
        <el-button type="primary" @click="handleRefresh">
          <i class="el-icon-refresh"></i> 刷新
        </el-button>
      </div>
    </div>

    <!-- 表格 -->
    <el-card shadow="never">
      <el-table
        v-loading="loading"
        :data="users"
        border
        stripe
        style="width: 100%"
        empty-text="暂无用户数据"
      >
        <el-table-column prop="id" label="用户ID" width="80" align="center" />
        <el-table-column prop="mobile" label="手机号" width="130" />
        <el-table-column prop="bonus_credits" label="剩余免费审查次数" width="140" align="center" />
        <el-table-column prop="status" label="账号状态" width="100" align="center">
          <template #default="{ row }">
            <el-tag :type="row.status === 'normal' ? 'success' : 'danger'" size="small">
              {{ row.status === 'normal' ? '正常' : '封禁' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="注册时间" width="170">
          <template #default="{ row }">
            {{ formatTime(row.created_at) }}
          </template>
        </el-table-column>
        <el-table-column prop="last_active_at" label="最后活跃时间" width="170">
          <template #default="{ row }">
            {{ row.last_active_at ? formatTime(row.last_active_at) : '-' }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="280" align="center" fixed="right">
          <template #default="{ row }">
            <el-button
              v-if="row.status === 'normal'"
              type="danger"
              text
              size="small"
              @click="handleBan(row)"
            >
              <i class="el-icon-ban"></i> 封禁
            </el-button>
            <el-button
              v-else
              type="success"
              text
              size="small"
              @click="handleUnban(row)"
            >
              <i class="el-icon-check"></i> 解封
            </el-button>
            <el-button type="primary" text size="small" @click="handleAddCredits(row)">
              <i class="el-icon-plus"></i> 增加额度
            </el-button>
            <el-button type="warning" text size="small" @click="handleReduceCredits(row)">
              <i class="el-icon-minus"></i> 减少额度
            </el-button>
            <el-button type="info" text size="small" @click="handleViewDetail(row)">
              <i class="el-icon-user"></i> 详情
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页 -->
      <div class="pagination-wrapper">
        <el-pagination
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :page-sizes="[10, 20, 50, 100]"
          :total="total"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="handleFilter"
          @current-change="handleFilter"
        />
      </div>
    </el-card>

    <!-- 封禁确认弹窗 -->
    <el-dialog
      v-model="banVisible"
      title="封禁用户"
      width="400px"
      :close-on-click-modal="false"
    >
      <p>确定要封禁用户 {{ banUserInfo.mobile }} 吗？</p>
      <el-form-item label="封禁理由">
        <el-input v-model="banReason" type="textarea" placeholder="请输入封禁理由" />
      </el-form-item>
      <template #footer>
        <el-button @click="banVisible = false">取消</el-button>
        <el-button type="danger" @click="confirmBan">确定封禁</el-button>
      </template>
    </el-dialog>

    <!-- 解封确认弹窗 -->
    <el-dialog
      v-model="unbanVisible"
      title="解封用户"
      width="400px"
      :close-on-click-modal="false"
    >
      <p>确定要解封用户 {{ unbanUserInfo.mobile }} 吗？</p>
      <el-form-item label="解封理由">
        <el-input v-model="unbanReason" type="textarea" placeholder="请输入解封理由" />
      </el-form-item>
      <template #footer>
        <el-button @click="unbanVisible = false">取消</el-button>
        <el-button type="primary" @click="confirmUnban">确定解封</el-button>
      </template>
    </el-dialog>

    <!-- 增加额度弹窗 -->
    <el-dialog
      v-model="addCreditsVisible"
      title="增加额度"
      width="400px"
      :close-on-click-modal="false"
    >
      <p>当前剩余额度：{{ addCreditsUserInfo.bonus_credits }} 次</p>
      <el-form-item label="增加数量">
        <el-input-number v-model="addCreditsAmount" :min="1" :max="100" />
      </el-form-item>
      <el-form-item label="操作理由">
        <el-input v-model="addCreditsReason" placeholder="请输入操作理由（可选）" />
      </el-form-item>
      <template #footer>
        <el-button @click="addCreditsVisible = false">取消</el-button>
        <el-button type="primary" @click="confirmAddCredits">确定增加</el-button>
      </template>
    </el-dialog>

    <!-- 减少额度弹窗 -->
    <el-dialog
      v-model="reduceCreditsVisible"
      title="减少额度"
      width="400px"
      :close-on-click-modal="false"
    >
      <p>当前剩余额度：{{ reduceCreditsUserInfo.bonus_credits }} 次</p>
      <el-form-item label="减少数量">
        <el-input-number v-model="reduceCreditsAmount" :min="1" :max="reduceCreditsUserInfo.bonus_credits || 1" />
      </el-form-item>
      <el-form-item label="操作理由">
        <el-input v-model="reduceCreditsReason" placeholder="请输入操作理由（可选）" />
      </el-form-item>
      <template #footer>
        <el-button @click="reduceCreditsVisible = false">取消</el-button>
        <el-button type="warning" @click="confirmReduceCredits">确定减少</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import {
  getUsers,
  banUser,
  unbanUser,
  addUserCredits,
  reduceUserCredits
} from '../../api/admin'

const router = useRouter()

// 筛选条件
const filterMobile = ref('')
const filterStatus = ref('')
const currentPage = ref(1)
const pageSize = ref(20)
const total = ref(0)
const users = ref([])
const loading = ref(false)

// 弹窗状态
const banVisible = ref(false)
const unbanVisible = ref(false)
const addCreditsVisible = ref(false)
const reduceCreditsVisible = ref(false)

// 弹窗数据
const banUserInfo = ref({ id: 0, mobile: '' })
const banReason = ref('')
const unbanUserInfo = ref({ id: 0, mobile: '' })
const unbanReason = ref('')
const addCreditsUserInfo = ref({ id: 0, mobile: '', bonus_credits: 0 })
const addCreditsAmount = ref(1)
const addCreditsReason = ref('')
const reduceCreditsUserInfo = ref({ id: 0, mobile: '', bonus_credits: 0 })
const reduceCreditsAmount = ref(1)
const reduceCreditsReason = ref('')

function formatTime(isoStr) {
  if (!isoStr) return '-'
  try {
    const d = new Date(isoStr)
    const pad = n => String(n).padStart(2, '0')
    return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())} ${pad(d.getHours())}:${pad(d.getMinutes())}:${pad(d.getSeconds())}`
  } catch {
    return isoStr
  }
}

async function loadUsers() {
  loading.value = true
  try {
    const params = {
      page: currentPage.value,
      size: pageSize.value
    }
    if (filterMobile.value) params.mobile = filterMobile.value
    if (filterStatus.value) params.status = filterStatus.value
    
    const res = await getUsers(params)
    if (res.success) {
      users.value = res.data || []
      total.value = res.total || 0
    } else {
      ElMessage.error(res.detail || '获取用户列表失败')
    }
  } catch (e) {
    console.error('加载用户列表失败:', e)
    ElMessage.error('加载失败，请检查网络或管理员Token')
  } finally {
    loading.value = false
  }
}

function handleFilter() {
  currentPage.value = 1
  loadUsers()
}

function handleRefresh() {
  filterMobile.value = ''
  filterStatus.value = ''
  handleFilter()
}

function handleBan(row) {
  banUserInfo.value = { id: row.id, mobile: row.mobile }
  banReason.value = ''
  banVisible.value = true
}

function handleUnban(row) {
  unbanUserInfo.value = { id: row.id, mobile: row.mobile }
  unbanReason.value = ''
  unbanVisible.value = true
}

function handleAddCredits(row) {
  addCreditsUserInfo.value = { id: row.id, mobile: row.mobile, bonus_credits: row.bonus_credits }
  addCreditsAmount.value = 1
  addCreditsReason.value = ''
  addCreditsVisible.value = true
}

function handleReduceCredits(row) {
  reduceCreditsUserInfo.value = { id: row.id, mobile: row.mobile, bonus_credits: row.bonus_credits }
  reduceCreditsAmount.value = 1
  reduceCreditsReason.value = ''
  reduceCreditsVisible.value = true
}

function handleViewDetail(row) {
  router.push(`/admin/users/${row.id}`)
}

async function confirmBan() {
  loading.value = true
  try {
    const res = await banUser(banUserInfo.value.id, banReason.value)
    if (res.success) {
      ElMessage.success('封禁成功')
      banVisible.value = false
      loadUsers()
    } else {
      ElMessage.error(res.detail || '封禁失败')
    }
  } catch (e) {
    console.error('封禁失败:', e)
    ElMessage.error('封禁失败')
  } finally {
    loading.value = false
  }
}

async function confirmUnban() {
  loading.value = true
  try {
    const res = await unbanUser(unbanUserInfo.value.id, unbanReason.value)
    if (res.success) {
      ElMessage.success('解封成功')
      unbanVisible.value = false
      loadUsers()
    } else {
      ElMessage.error(res.detail || '解封失败')
    }
  } catch (e) {
    console.error('解封失败:', e)
    ElMessage.error('解封失败')
  } finally {
    loading.value = false
  }
}

async function confirmAddCredits() {
  loading.value = true
  try {
    const res = await addUserCredits(addCreditsUserInfo.value.id, addCreditsAmount.value, addCreditsReason.value)
    if (res.success) {
      ElMessage.success(`成功增加 ${addCreditsAmount.value} 次免费审查额度`)
      addCreditsVisible.value = false
      loadUsers()
    } else {
      ElMessage.error(res.detail || '增加额度失败')
    }
  } catch (e) {
    console.error('增加额度失败:', e)
    ElMessage.error('增加额度失败')
  } finally {
    loading.value = false
  }
}

async function confirmReduceCredits() {
  loading.value = true
  try {
    const res = await reduceUserCredits(reduceCreditsUserInfo.value.id, reduceCreditsAmount.value, reduceCreditsReason.value)
    if (res.success) {
      ElMessage.success(`成功减少 ${reduceCreditsAmount.value} 次免费审查额度`)
      reduceCreditsVisible.value = false
      loadUsers()
    } else {
      ElMessage.error(res.detail || '减少额度失败')
    }
  } catch (e) {
    console.error('减少额度失败:', e)
    ElMessage.error('减少额度失败')
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadUsers()
})
</script>

<style scoped>
.user-list-page {
  padding: 0;
}

.filter-bar {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 16px;
  flex-wrap: wrap;
}

.filter-item {
  display: flex;
  align-items: center;
  gap: 8px;
}

.filter-label {
  font-size: 14px;
  color: #606266;
  white-space: nowrap;
}

.pagination-wrapper {
  display: flex;
  justify-content: flex-end;
  margin-top: 16px;
}
</style>