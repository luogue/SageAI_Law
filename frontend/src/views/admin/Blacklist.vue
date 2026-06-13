<template>
  <div class="blacklist-page">
    <!-- 统计卡片 -->
    <el-card class="stats-card">
      <div class="stats-row">
        <div class="stat-item">
          <p class="stat-value">{{ blacklistCount }}</p>
          <p class="stat-label">黑名单总数</p>
        </div>
        <div class="stat-item">
          <p class="stat-value">{{ autoBanStats.last_24h || 0 }}</p>
          <p class="stat-label">近24小时自动封禁</p>
        </div>
      </div>
    </el-card>
    
    <!-- 添加黑名单表单 -->
    <el-card class="form-card">
      <h3>添加黑名单</h3>
      <el-form :model="addForm" inline>
        <el-form-item label="类型">
          <el-select v-model="addForm.type" placeholder="请选择类型">
            <el-option label="IP" value="ip" />
            <el-option label="用户ID" value="user_id" />
          </el-select>
        </el-form-item>
        <el-form-item label="值">
          <el-input v-model="addForm.value" placeholder="请输入IP或用户ID" />
        </el-form-item>
        <el-form-item label="原因">
          <el-input v-model="addForm.reason" placeholder="封禁原因（选填）" />
        </el-form-item>
        <el-form-item label="过期时间">
          <el-date-picker 
            v-model="addForm.expiresAt" 
            type="datetime" 
            placeholder="不填则永久"
          />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleAdd">添加</el-button>
        </el-form-item>
      </el-form>
    </el-card>
    
    <!-- 黑名单列表 -->
    <el-card>
      <h3>黑名单列表</h3>
      <el-table :data="blacklist" border>
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column 
          prop="type" 
          label="类型" 
          width="100"
          :formatter="formatType"
        />
        <el-table-column prop="value" label="值" />
        <el-table-column prop="reason" label="原因" />
        <el-table-column prop="created_at" label="封禁时间" width="160" />
        <el-table-column 
          prop="expires_at" 
          label="过期时间" 
          width="160"
          :formatter="formatExpiresAt"
        />
        <el-table-column label="操作" width="100">
          <template #default="scope">
            <el-button size="small" type="danger" @click="handleRemove(scope.row)">解除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { getBlacklist, addToBlacklist, removeFromBlacklist, getAutoBanStats } from '../../api/admin'

const blacklist = ref([])
const blacklistCount = ref(0)
const autoBanStats = reactive({ last_24h: 0 })

const addForm = reactive({
  type: '',
  value: '',
  reason: '',
  expiresAt: null
})

async function loadBlacklist() {
  try {
    const result = await getBlacklist()
    blacklist.value = result.data
    blacklistCount.value = result.count
  } catch (e) {
    console.error('加载黑名单失败:', e)
  }
}

async function loadAutoBanStats() {
  try {
    const result = await getAutoBanStats(24)
    autoBanStats.last_24h = result.data.last_24h || 0
  } catch (e) {
    console.error('加载自动封禁统计失败:', e)
  }
}

async function handleAdd() {
  if (!addForm.type || !addForm.value) {
    return
  }
  
  try {
    const expiresAt = addForm.expiresAt ? addForm.expiresAt.toISOString() : null
    await addToBlacklist(addForm.type, addForm.value, addForm.reason, expiresAt)
    addForm.type = ''
    addForm.value = ''
    addForm.reason = ''
    addForm.expiresAt = null
    loadBlacklist()
  } catch (e) {
    console.error('添加黑名单失败:', e)
  }
}

async function handleRemove(row) {
  try {
    await removeFromBlacklist(row.type, row.value)
    loadBlacklist()
  } catch (e) {
    console.error('移除黑名单失败:', e)
  }
}

function formatType(row) {
  return row.type === 'ip' ? 'IP' : '用户ID'
}

function formatExpiresAt(row) {
  if (!row.expires_at) return '永久'
  return row.expires_at
}

onMounted(() => {
  loadBlacklist()
  loadAutoBanStats()
})
</script>

<style scoped>
.blacklist-page {
  padding: 20px;
}

.stats-card {
  margin-bottom: 16px;
}

.stats-row {
  display: flex;
  gap: 40px;
}

.stat-item {
  text-align: center;
}

.stat-value {
  font-size: 28px;
  font-weight: bold;
  margin: 0 0 4px 0;
  color: #303133;
}

.stat-label {
  font-size: 14px;
  color: #909399;
  margin: 0;
}

.form-card {
  margin-bottom: 16px;
}

.form-card h3 {
  font-size: 16px;
  margin: 0 0 16px 0;
  color: #303133;
}
</style>
