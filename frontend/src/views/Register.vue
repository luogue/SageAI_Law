<template>
  <div class="register-container">
    <!-- 新手大礼包 -->
    <div class="newbie-gift">
      <div class="gift-icon">🎁</div>
      <div class="gift-content">
        <span class="gift-title">新手大礼包</span>
        <span class="gift-desc">新用户注册即送3次免费审查额度，无使用期限</span>
      </div>
    </div>

    <div class="register-card">
      <div class="logo-section">
        <svg width="64" height="64" viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg">
          <rect x="8" y="8" width="48" height="48" rx="8" stroke="#4080FF" stroke-width="2"/>
          <path d="M20 32h12M32 32h12M20 40h8M28 40h8M20 24h8M28 24h8" stroke="#4080FF" stroke-width="2" stroke-linecap="round"/>
        </svg>
        <h1>明月AI（Sage）合同审查</h1>
        <p>智能合同审查，助力合规决策</p>
      </div>

      <el-form ref="formRef" :model="formData" class="register-form">
        <div class="form-title">
          <span class="active">注册</span>
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

        <!-- 验证码 -->
        <el-form-item label="验证码" prop="smsCode">
          <div class="code-input-wrapper">
            <el-input 
              v-model="formData.smsCode" 
              type="tel" 
              placeholder="请输入6位验证码"
              maxlength="6"
              :disabled="isSubmitting"
            />
            <button 
              type="button"
              class="get-code-btn"
              @click="handleSendCode"
              :disabled="isSubmitting || !isPhoneValid || countdown > 0"
            >
              {{ countdown > 0 ? `${countdown}秒后重新获取` : '获取验证码' }}
            </button>
          </div>
        </el-form-item>

        <!-- 密码 -->
        <el-form-item label="密码" prop="password">
          <el-input 
            v-model="formData.password" 
            type="password" 
            placeholder="请设置登录密码"
            :disabled="isSubmitting"
            @input="checkPasswordStrength"
          />
          <div v-if="passwordStrength" class="password-strength">
            <span>密码强度：</span>
            <span :class="passwordStrength.class">{{ passwordStrength.text }}</span>
          </div>
        </el-form-item>

        <!-- 确认密码 -->
        <el-form-item label="确认密码" prop="confirmPassword">
          <el-input 
            v-model="formData.confirmPassword" 
            type="password" 
            placeholder="请再次输入密码"
            :disabled="isSubmitting"
          />
        </el-form-item>

        <!-- 协议勾选 -->
        <div class="agreement-section">
          <el-checkbox v-model="agreedToTerms" :disabled="isSubmitting">
            我已阅读并同意
            <a href="#" @click.prevent="$emit('show-terms')">《用户服务协议》</a>
            和
            <a href="#" @click.prevent="$emit('show-privacy')">《隐私政策》</a>
          </el-checkbox>
        </div>

        <!-- 注册赠送提示 -->
        <div class="bonus-notice">
          <span class="gift-icon">🎁</span>
          <span>新用户注册即赠送3次免费审查额度，不设有效期，用完为止</span>
        </div>

        <!-- 注册按钮 -->
        <el-form-item>
          <el-button 
            class="submit-btn"
            type="primary" 
            @click="handleSubmit"
            :disabled="!canSubmit || isSubmitting"
            :loading="isSubmitting"
          >
            注册
          </el-button>
        </el-form-item>
      </el-form>
      
      <!-- 底部链接 -->
      <div class="footer-links">
        <span>已有账号？</span>
        <a href="#" @click.prevent="router.push('/login')">立即登录</a>
        <span class="divider">|</span>
        <a href="#" @click="handleShowPrivacy">隐私政策</a>
        <span class="divider">|</span>
        <a href="#" @click="handleShowTerms">用户协议</a>
      </div>
    </div>

    <!-- 滑动验证码组件 -->
    <SliderCaptcha
      :visible="showCaptcha"
      @success="handleCaptchaSuccess"
      @close="handleCaptchaClose"
    />
    
    <!-- 隐私政策弹窗 -->
    <PrivacyPolicy v-if="showPrivacyModal" @close="showPrivacyModal = false" />
    
    <!-- 用户协议弹窗 -->
    <TermsOfService v-if="showTermsModal" @close="showTermsModal = false" />
  </div>
</template>

<script setup>
import { ref, computed, reactive, onBeforeUnmount, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import { register, sendSmsCode } from '../utils/api'
import SliderCaptcha from '../components/SliderCaptcha.vue'
import PhoneInput from '../components/PhoneInput.vue'
import PrivacyPolicy from '../components/PrivacyPolicy.vue'
import TermsOfService from '../components/TermsOfService.vue'

const router = useRouter()
const route = useRoute()

// 从 URL 查询参数中获取邀请人 ID
const inviterId = ref(route.query.inviter_id || null)
if (inviterId.value) {
  console.log('[Register] 检测到邀请链接，inviter_id:', inviterId.value)
  ElMessage.info('您正在通过好友邀请注册，注册成功后双方均可获得额外额度！')
}
const emit = defineEmits(['register-success'])

const isSubmitting = ref(false)
const showCaptcha = ref(false)
const countdown = ref(0)
const agreedToTerms = ref(false)
const isPhoneValid = ref(false)
const phoneError = ref('')
const showPrivacyModal = ref(false)
const showTermsModal = ref(false)
let countdownTimer = null

const formData = reactive({
  phone: '',
  smsCode: '',
  password: '',
  confirmPassword: ''
})

const passwordStrength = ref(null)

const canSubmit = computed(() => {
  return formData.phone &&
         formData.smsCode && formData.smsCode.length === 6 &&
         formData.password && formData.password.length >= 6 &&
         formData.confirmPassword &&
         formData.password === formData.confirmPassword &&
         agreedToTerms.value &&
         !isSubmitting.value
})

const validateMobile = (mobile = formData.phone) => {
  // 国际手机号校验：区号+数字，去除非数字后总长度在 10-15 位之间
  const digits = mobile.replace(/\D/g, '')
  isPhoneValid.value = digits.length >= 10 && digits.length <= 15
  return isPhoneValid.value
}

const handlePhoneValidate = ({ valid, message }) => {
  isPhoneValid.value = valid
  phoneError.value = valid ? '' : message
}

const checkPasswordStrength = () => {
  const password = formData.password
  if (!password) {
    passwordStrength.value = null
    return
  }
  
  let score = 0
  
  // 长度 >= 6
  if (password.length >= 6) score++
  if (password.length >= 10) score++
  
  // 包含数字
  if (/[0-9]/.test(password)) score++
  
  // 包含小写字母
  if (/[a-z]/.test(password)) score++
  
  // 包含大写字母
  if (/[A-Z]/.test(password)) score++
  
  // 包含特殊字符
  if (/[!@#$%^&*()_+\-=\[\]{}|;:,.<>?]/.test(password)) score++
  
  if (score <= 2) {
    passwordStrength.value = { text: '弱', class: 'weak' }
  } else if (score <= 4) {
    passwordStrength.value = { text: '中', class: 'medium' }
  } else {
    passwordStrength.value = { text: '强', class: 'strong' }
  }
}

const handleSendCode = async () => {
  if (!validateMobile()) {
    ElMessage.error('请输入正确的手机号')
    return
  }
  
  // 显示滑动验证码
  showCaptcha.value = true
}

const handleCaptchaSuccess = async (captchaToken) => {
  showCaptcha.value = false
  isSubmitting.value = true
  
  try {
    await sendSmsCode(formData.phone, captchaToken)
    ElMessage.success('验证码已发送，请注意查收')
    
    // 清除之前的定时器
    if (countdownTimer) {
      clearInterval(countdownTimer)
    }
    
    // 开始倒计时
    countdown.value = 60
    countdownTimer = setInterval(() => {
      countdown.value--
      if (countdown.value <= 0) {
        clearInterval(countdownTimer)
        countdownTimer = null
      }
    }, 1000)
  } catch (error) {
    ElMessage.error(error.message || '发送验证码失败')
  } finally {
    isSubmitting.value = false
  }
}

const handleCaptchaClose = () => {
  showCaptcha.value = false
}

const handleSubmit = async () => {
  phoneError.value = ''
  
  // 验证手机号
  if (!validateMobile()) {
    ElMessage.error('请输入正确的手机号')
    return
  }
  
  // 验证密码强度
  if (formData.password.length < 6) {
    ElMessage.error('密码长度至少6位')
    return
  }
  
  // 验证密码一致性
  if (formData.password !== formData.confirmPassword) {
    ElMessage.error('两次输入的密码不一致')
    return
  }
  
  isSubmitting.value = true
  
  try {
    const response = await register(
      formData.phone,
      formData.smsCode,
      formData.password,
      formData.confirmPassword,
      inviterId.value  // 传递邀请人ID
    )
    
    // 存储token
    localStorage.setItem('token', response.access_token)
    localStorage.setItem('user_id', response.user_id.toString())
    localStorage.setItem('user_mobile', response.mobile)
    
    // 清空表单
    formData.phone = ''
    formData.smsCode = ''
    formData.password = ''
    formData.confirmPassword = ''
    
    ElMessage.success('注册成功，已赠送3次免费审查额度')
    router.push('/')
  } catch (error) {
    ElMessage.error(error.message || '注册失败')
  } finally {
    isSubmitting.value = false
  }
}

const handleShowPrivacy = () => {
  console.log('显示隐私政策')
  showPrivacyModal.value = true
}

const handleShowTerms = () => {
  console.log('显示用户协议')
  showTermsModal.value = true
}
</script>

<style scoped>
.register-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background: #FEFEFE;
  padding: 20px;
}

.register-card {
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

.register-form {
  width: 100%;
}

.register-form :deep(.el-form-item) {
  margin-bottom: 18px;
  display: flex;
  align-items: flex-start;
}

.register-form :deep(.el-form-item__label) {
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

.register-form :deep(.el-form-item__content) {
  flex: 1;
  min-width: 0;
}

.register-form :deep(.el-input) {
  width: 100%;
}

.register-form :deep(.el-input__inner) {
  height: 40px;
}

.register-form :deep(.code-input-wrapper) {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-wrap: nowrap;
}

.register-form :deep(.code-input-wrapper .el-input) {
  flex: 1;
  min-width: 0;
}

.get-code-btn {
  padding: 0 16px;
  height: 40px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: opacity 0.2s;
  white-space: nowrap;
  flex-shrink: 0;
}

.get-code-btn:hover:not(:disabled) {
  opacity: 0.9;
}

.get-code-btn:disabled {
  background: #ccc;
  cursor: not-allowed;
}

.password-strength {
  margin-top: 8px;
  font-size: 13px;
  color: #666;
}

.password-strength .weak {
  color: #ff6b6b;
}

.password-strength .medium {
  color: #ffa502;
}

.password-strength .strong {
  color: #2ed573;
}

.agreement-section {
  margin: 16px 0;
  font-size: 13px;
}

.agreement-section a {
  color: #4080FF;
  text-decoration: none;
}

.agreement-section a:hover {
  text-decoration: underline;
}

.bonus-notice {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 16px;
  background: #fff7e6;
  border-radius: 8px;
  font-size: 13px;
  color: #d48806;
  margin: 16px 0;
}

.bonus-notice .gift-icon {
  font-size: 16px;
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
  .register-card {
    padding: 24px 16px;
    border-radius: 12px;
  }

  .logo-section h1 {
    font-size: 20px;
  }

  .register-form :deep(.el-form-item__label) {
    width: 70px !important;
    min-width: 70px;
    padding-right: 8px;
    font-size: 13px;
  }

  .get-code-btn {
    padding: 10px 14px;
    font-size: 13px;
  }
}

@media (max-width: 360px) {
  .register-form :deep(.el-form-item__label) {
    width: 60px !important;
    min-width: 60px;
  }
}
</style>
