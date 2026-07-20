<template>
  <div class="login-container">
    <div class="login-card">
      <div class="logo-section">
        <svg width="64" height="64" viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg">
          <rect x="8" y="8" width="48" height="48" rx="8" stroke="#4080FF" stroke-width="2"/>
          <path d="M20 32h12M32 32h12M20 40h8M28 40h8M20 24h8M28 24h8" stroke="#4080FF" stroke-width="2" stroke-linecap="round"/>
        </svg>
        <h1>明月AI（Sage）合同审查</h1>
        <p>智能合同审查，助力合规决策</p>
      </div>

      <el-form ref="formRef" :model="formData" class="login-form">
        <div class="form-title">
          <span class="active">登录</span>
        </div>

        <!-- 手机号 -->
        <el-form-item label="手机号" prop="phone" :error="phoneError">
          <PhoneInput
            v-model="formData.phone"
            :disabled="isSubmitting"
            :has-error="!!phoneError"
            placeholder="请输入手机号"
            @validate="handlePhoneValidate"
          />
        </el-form-item>

        <!-- 密码 -->
        <el-form-item label="密码" prop="password">
          <el-input 
            v-model="formData.password" 
            type="password" 
            placeholder="请输入密码"
            :disabled="isSubmitting"
          />
        </el-form-item>

        <!-- 登录按钮 -->
        <el-form-item>
          <el-button 
            class="submit-btn"
            type="primary" 
            @click="handleSubmit"
            :disabled="!canSubmit || isSubmitting"
            :loading="isSubmitting"
          >
            登录
          </el-button>
        </el-form-item>
      </el-form>
      
      <!-- 底部链接 -->
      <div class="footer-links">
        <span>新用户请由管理员创建账号</span>
        <span class="divider">|</span>
        <a href="#" @click="handleShowPrivacy">隐私政策</a>
        <span class="divider">|</span>
        <a href="#" @click="handleShowTerms">用户协议</a>
      </div>
    </div>
    
    <!-- 隐私政策弹窗 -->
    <PrivacyPolicy v-if="showPrivacyModal" @close="showPrivacyModal = false" />
    
    <!-- 用户协议弹窗 -->
    <TermsOfService v-if="showTermsModal" @close="showTermsModal = false" />
  </div>
</template>

<script setup>
import { ref, computed, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { login } from '../utils/api'
import PhoneInput from '../components/PhoneInput.vue'
import PrivacyPolicy from '../components/PrivacyPolicy.vue'
import TermsOfService from '../components/TermsOfService.vue'

const router = useRouter()
const emit = defineEmits(['login-success'])

const isSubmitting = ref(false)
const phoneError = ref('')
const isPhoneValid = ref(false)
const showPrivacyModal = ref(false)
const showTermsModal = ref(false)

const formData = reactive({
  phone: '',
  password: ''
})

const canSubmit = computed(() => {
  return isPhoneValid.value && formData.password && !isSubmitting.value
})

const handleShowPrivacy = () => {
  console.log('显示隐私政策')
  showPrivacyModal.value = true
}

const handleShowTerms = () => {
  console.log('显示用户协议')
  showTermsModal.value = true
}

const handlePhoneValidate = ({ valid, message }) => {
  isPhoneValid.value = valid
  phoneError.value = valid ? '' : message
}

const validateMobile = (mobile) => {
  // 国际手机号校验：去除非数字后总长度在 10-15 位之间
  const digits = mobile.replace(/\D/g, '')
  return digits.length >= 10 && digits.length <= 15
}

const handleSubmit = async () => {
  phoneError.value = ''

  // 验证手机号
  if (!validateMobile(formData.phone)) {
    ElMessage.error('请输入正确的手机号')
    return
  }
  
  isSubmitting.value = true
  
  try {
    const response = await login(formData.phone, formData.password)
    
    // 存储token
    localStorage.setItem('token', response.access_token)
    localStorage.setItem('user_id', response.user_id.toString())
    localStorage.setItem('user_mobile', response.mobile)
    
    // 清空表单
    formData.phone = ''
    formData.password = ''
    
    ElMessage.success('登录成功')
    router.push('/')
  } catch (error) {
    ElMessage.error(error.message || '登录失败')
  } finally {
    isSubmitting.value = false
  }
}
</script>

<style scoped>
.login-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background: #FEFEFE;
  padding: 20px;
}

.login-card {
  background: white;
  border-radius: 16px;
  padding: 40px;
  width: 100%;
  max-width: 420px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.15);
}

.logo-section {
  text-align: center;
  margin-bottom: 32px;
}

.logo-section h1 {
  margin: 16px 0 8px;
  font-size: 24px;
  color: #333;
  font-weight: 600;
}

.logo-section p {
  color: #999;
  font-size: 14px;
}

.form-title {
  text-align: center;
  margin-bottom: 24px;
  font-size: 18px;
}

.form-title span.active {
  color: #4080FF;
  font-weight: 600;
}

.login-form {
  width: 100%;
}

.login-form :deep(.el-form-item) {
  margin-bottom: 24px;
  display: flex;
  align-items: flex-start;
}

.login-form :deep(.el-form-item__content) {
  flex: 1;
  min-width: 0;
}

.login-form :deep(.el-form-item__label) {
  width: 80px !important;
  min-width: 80px;
  max-width: 80px;
  text-align: right;
  padding-right: 12px;
  color: #606266;
  font-size: 14px;
  font-weight: 500;
  flex-shrink: 0;
  flex-basis: 80px;
  padding-top: 10px;
}

.login-form :deep(.el-input) {
  width: 100%;
}

.login-form :deep(.el-input__inner) {
  height: 40px;
}



.submit-btn {
  width: 100%;
  height: 44px;
  font-size: 16px;
  font-weight: 600;
}

.error-message {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #ff6b6b;
  font-size: 13px;
  padding: 12px;
  background: #fff5f5;
  border-radius: 8px;
  margin-bottom: 16px;
}

.error-icon {
  font-weight: bold;
}

.footer-links {
  text-align: center;
  margin-top: 20px;
  font-size: 14px;
  position: relative;
  z-index: 100;
  pointer-events: auto;
}

.footer-links a {
  color: #4080FF;
  text-decoration: none;
  margin: 0 8px;
  cursor: pointer;
  display: inline-block;
  position: relative;
  z-index: 101;
  pointer-events: auto;
  padding: 5px 10px;
}

.footer-links a:hover {
  text-decoration: underline;
}

.footer-links .divider {
  color: #e8e8e8;
  user-select: none;
  pointer-events: none;
}

.newbie-gift {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 20px;
  background: linear-gradient(135deg, #ff6b6b 0%, #feca57 100%);
  border-radius: 10px;
  box-shadow: 0 4px 15px rgba(255, 107, 107, 0.3);
  margin-bottom: 20px;
}

.newbie-gift .gift-icon {
  font-size: 32px;
  animation: bounce 2s infinite;
}

.newbie-gift .gift-content {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.newbie-gift .gift-title {
  font-size: 15px;
  font-weight: 700;
  color: white;
}

.newbie-gift .gift-desc {
  font-size: 13px;
  color: rgba(255, 255, 255, 0.9);
}

@keyframes bounce {
  0%, 20%, 50%, 80%, 100% {
    transform: translateY(0);
  }
  40% {
    transform: translateY(-10px);
  }
  60% {
    transform: translateY(-5px);
  }
}

/* 移动端适配 */
@media (max-width: 480px) {
  .login-card {
    padding: 24px 16px;
    border-radius: 12px;
  }

  .logo-section h1 {
    font-size: 20px;
  }

  .login-form :deep(.el-form-item__label) {
    width: 70px !important;
    min-width: 70px;
    padding-right: 8px;
    font-size: 13px;
  }
}

@media (max-width: 360px) {
  .login-form :deep(.el-form-item__label) {
    width: 60px !important;
    min-width: 60px;
  }
}
</style>
