<template>
  <div class="admin-login-container">
    <div class="login-box">
      <div class="logo">
        <h1>SageAI 管理后台</h1>
        <p class="subtitle">明月AI 管理员登录</p>
      </div>
      
      <el-form ref="loginForm" :model="form" :rules="rules" class="login-form">
        <el-form-item prop="phone">
          <el-input 
            v-model="form.phone" 
            placeholder="手机号" 
            prefix-icon="el-icon-user"
            size="large"
          />
        </el-form-item>
        
        <el-form-item prop="password">
          <el-input 
            v-model="form.password" 
            type="password" 
            placeholder="密码" 
            prefix-icon="el-icon-lock"
            size="large"
            @keyup.enter="handleLogin"
          />
        </el-form-item>
        
        <el-form-item>
          <el-button 
            type="primary" 
            size="large" 
            class="login-btn"
            :loading="loading"
            @click="handleLogin"
          >
            登录
          </el-button>
        </el-form-item>
      </el-form>
      
      <p v-if="error" class="error-message">{{ error }}</p>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { adminLogin } from '../../api/admin'

const form = reactive({
  phone: '',
  password: ''
})

const loading = ref(false)
const error = ref('')

const rules = {
  phone: [
    { required: true, message: '请输入手机号', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' }
  ]
}

async function handleLogin() {
  loading.value = true
  error.value = ''
  
  try {
    const result = await adminLogin(form.phone, form.password)
    if (result.success) {
      localStorage.setItem('admin_token', result.token)
      localStorage.setItem('admin_username', result.username)
      window.location.href = '/admin'
    } else {
      error.value = result.detail || '登录失败'
    }
  } catch (e) {
    error.value = e.message || '登录失败'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.admin-login-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.login-box {
  width: 400px;
  padding: 40px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.15);
}

.logo {
  text-align: center;
  margin-bottom: 30px;
}

.logo h1 {
  font-size: 24px;
  color: #303133;
  margin: 0 0 8px 0;
}

.subtitle {
  font-size: 14px;
  color: #909399;
  margin: 0;
}

.login-form {
  margin-bottom: 16px;
}

.login-btn {
  width: 100%;
  height: 44px;
}

.error-message {
  text-align: center;
  color: #f56c6c;
  font-size: 14px;
  margin: 0;
}
</style>
