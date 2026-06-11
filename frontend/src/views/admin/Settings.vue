<template>
  <div class="settings-page">
    <el-card>
      <h3>系统设置</h3>
      
      <el-form :model="settings" label-width="180px">
        <el-form-item label="管理员用户名">
          <el-input :value="settings.admin_username" disabled />
        </el-form-item>
        
        <el-form-item label="默认奖励额度">
          <el-input-number 
            :model-value="settings.default_bonus_credits" 
            :min="1" 
            :max="10" 
            :step="1"
            disabled
          />
          <span class="unit">次免费审查额度</span>
        </el-form-item>
        
        <el-form-item label="自动封禁">
          <el-switch 
            :value="settings.auto_ban_enable" 
            disabled
          />
          <span class="hint">控制是否启用自动封禁功能</span>
        </el-form-item>
        
        <el-form-item label="阿里云内容安全">
          <el-switch 
            :value="settings.aliyun_green_enable" 
            disabled
          />
          <span class="hint">控制是否启用阿里云内容安全审核</span>
        </el-form-item>
      </el-form>
      
      <div class="settings-note">
        <h4>修改配置说明</h4>
        <ul>
          <li>管理员用户名：通过环境变量 <code>ADMIN_USERNAME</code> 设置</li>
          <li>管理员密码：通过环境变量 <code>ADMIN_PASSWORD</code> 设置</li>
          <li>默认奖励额度：通过环境变量 <code>DEFAULT_BONUS_CREDITS</code> 设置</li>
          <li>自动封禁开关：通过环境变量 <code>AUTO_BAN_ENABLE=true/false</code> 设置</li>
          <li>阿里云内容安全：通过环境变量 <code>ALIYUN_GREEN_ENABLE=true/false</code> 设置</li>
          <li>修改环境变量后需要重启后端服务才能生效</li>
        </ul>
      </div>
    </el-card>
    
    <!-- 白名单管理 -->
    <el-card class="whitelist-card">
      <div class="card-header">
        <h3>白名单管理</h3>
        <div class="add-word">
          <el-input 
            v-model="newWord" 
            placeholder="输入要添加的词" 
            style="width: 200px;"
            @keyup.enter="handleAddWhitelist"
          />
          <el-button type="primary" size="small" @click="handleAddWhitelist">添加</el-button>
        </div>
      </div>
      
      <el-table :data="whitelist" border>
        <el-table-column prop="word" label="白名单词" />
        <el-table-column label="操作" width="100">
          <template #default="scope">
            <el-button size="small" type="danger" @click="handleRemoveWhitelist(scope.row.word)">移除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { getSettings, getWhitelist, addWhitelistWord, removeWhitelistWord } from '../../api/admin'

const settings = reactive({
  admin_username: '',
  auto_ban_enable: false,
  aliyun_green_enable: false,
  default_bonus_credits: 3
})

const whitelist = ref([])
const newWord = ref('')

async function loadSettings() {
  try {
    const result = await getSettings()
    Object.assign(settings, result.data)
  } catch (e) {
    console.error('加载设置失败:', e)
  }
}

async function loadWhitelist() {
  try {
    const result = await getWhitelist()
    whitelist.value = result.data.map(word => ({ word }))
  } catch (e) {
    console.error('加载白名单失败:', e)
  }
}

async function handleAddWhitelist() {
  if (!newWord.value.trim()) return
  
  try {
    await addWhitelistWord(newWord.value.trim())
    newWord.value = ''
    loadWhitelist()
  } catch (e) {
    console.error('添加白名单失败:', e)
  }
}

async function handleRemoveWhitelist(word) {
  try {
    await removeWhitelistWord(word)
    loadWhitelist()
  } catch (e) {
    console.error('移除白名单失败:', e)
  }
}

onMounted(() => {
  loadSettings()
  loadWhitelist()
})
</script>

<style scoped>
.settings-page {
  padding: 20px;
}

.settings-page h3 {
  font-size: 16px;
  margin: 0 0 16px 0;
  color: #303133;
}

.unit {
  margin-left: 8px;
  color: #909399;
}

.hint {
  margin-left: 12px;
  color: #909399;
  font-size: 13px;
}

.settings-note {
  margin-top: 24px;
  padding: 16px;
  background: #f5f7fa;
  border-radius: 8px;
}

.settings-note h4 {
  margin: 0 0 12px 0;
  color: #303133;
}

.settings-note ul {
  margin: 0;
  padding-left: 20px;
}

.settings-note li {
  margin-bottom: 8px;
  color: #606266;
  font-size: 14px;
}

.settings-note code {
  background: #fff;
  padding: 2px 6px;
  border-radius: 4px;
  font-size: 13px;
}

.whitelist-card {
  margin-top: 16px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.card-header h3 {
  margin: 0;
}

.add-word {
  display: flex;
  gap: 8px;
}
</style>
