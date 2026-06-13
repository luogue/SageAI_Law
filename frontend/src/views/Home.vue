<template>
  <div class="app-container">
    <!-- 顶部导航 -->
    <header class="top-nav">
      <div class="nav-container">
        <div class="nav-brand">
          <svg width="28" height="28" viewBox="0 0 32 32" fill="none">
            <rect x="4" y="4" width="24" height="24" rx="4" stroke="#4080FF" stroke-width="2"/>
            <path d="M10 16h6M16 16h6M10 20h4M14 20h4M10 12h4M14 12h4" stroke="#4080FF" stroke-width="2" stroke-linecap="round"/>
          </svg>
          <span class="brand-text">明月AI（Sage）合同审查</span>
        </div>
        <div class="nav-links">
          <router-link 
            to="/" 
            class="nav-link-item" 
            :class="{ active: isActive('/') }"
            exact
          >
            上传审查
          </router-link>
          <span class="divider">|</span>
          <router-link 
            to="/reports" 
            class="nav-link-item" 
            :class="{ active: isActive('/reports') }"
          >
            我的报告
          </router-link>
          <span class="divider">|</span>
          <a href="#" class="nav-link-item" @click.prevent="showPrivacy">隐私政策</a>
          <span class="divider">|</span>
          <a href="#" class="nav-link-item" @click.prevent="showTerms">用户协议</a>
          <div class="credits-display" v-if="bonusCredits >= 0">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <circle cx="12" cy="12" r="10"/>
              <polyline points="12 6 12 12 16 14"/>
            </svg>
            <span class="credits-text">剩余免费额度：{{ bonusCredits }}次</span>
            <button class="get-more-credits-btn" @click="showCreditSupplyModal = true">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M12 5v14M5 12h14"/>
              </svg>
              <span>获取更多</span>
            </button>
          </div>
          <div class="user-mobile" v-if="maskedMobile">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M16 8a6 6 0 0 1 6 6v7h-4.5a3.5 3.5 0 0 0-3.5 3.5v0.5H10v-0.5A3.5 3.5 0 0 0 6.5 21H2v-7a6 6 0 0 1 6-6h2z"/>
              <circle cx="12" cy="10" r="3"/>
            </svg>
            <span class="mobile-text">{{ maskedMobile }}</span>
          </div>
          <button class="logout-btn-small" @click="handleLogout" title="退出登录">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/>
              <polyline points="16 17 21 12 16 7"/>
              <line x1="21" y1="12" x2="9" y2="12"/>
            </svg>
            <span>退出</span>
          </button>
        </div>
      </div>
    </header>

    <!-- 主内容区 -->
    <main class="main-content">
      <router-view v-slot="{ Component, route: childRoute }">
        <keep-alive :include="cachedComponents">
          <component 
            :is="Component" 
            :key="childRoute.name"
            @update-credits="handleUpdateCredits"
          />
        </keep-alive>
      </router-view>
    </main>

    <!-- 隐私政策弹窗 -->
    <PrivacyPolicy v-if="showPrivacyModal" @close="showPrivacyModal = false" />
    
    <!-- 用户协议弹窗 -->
    <TermsOfService v-if="showTermsModal" @close="showTermsModal = false" />
    
    <!-- 额度补给站模态框 -->
    <CreditSupplyModal 
      :visible="showCreditSupplyModal" 
      @close="showCreditSupplyModal = false"
      @open-feedback="handleOpenFeedback"
    />
    
    <!-- 反馈模态框 -->
    <FeedbackModal
      :show="showFeedbackModal"
      :report-id="''"
      :expected-file-hash="''"
      @close="showFeedbackModal = false"
      @success="handleFeedbackSuccess"
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import PrivacyPolicy from '../components/PrivacyPolicy.vue'
import TermsOfService from '../components/TermsOfService.vue'
import CreditSupplyModal from '../components/CreditSupplyModal.vue'
import FeedbackModal from '../components/FeedbackModal.vue'
import { getBonusCredits } from '../utils/api'

const router = useRouter()
const route = useRoute()

const showPrivacyModal = ref(false)
const showTermsModal = ref(false)
const showCreditSupplyModal = ref(false)
const showFeedbackModal = ref(false)
const bonusCredits = ref(0)

// 需要缓存的组件名称列表（对应 router.meta.keepAlive 标记的组件）
const cachedComponents = ref(['UploadPage'])

const maskedMobile = computed(() => {
  const mobile = localStorage.getItem('user_mobile')
  if (!mobile || mobile.length < 11) return null
  return mobile.substring(0, 3) + '****' + mobile.substring(7)
})

onMounted(() => {
  fetchBonusCredits()
})

const fetchBonusCredits = async () => {
  try {
    const response = await getBonusCredits()
    bonusCredits.value = response.bonus_credits
  } catch (error) {
    console.error('获取用户额度失败:', error)
  }
}

// 只在审查成功时更新额度（通过事件监听）
const handleUpdateCredits = (newCredits) => {
  bonusCredits.value = newCredits
}

const isActive = (path) => {
  return route.path === path
}

const handleLogout = () => {
  localStorage.removeItem('token')
  localStorage.removeItem('user_id')
  localStorage.removeItem('user_mobile')
  bonusCredits.value = 0
  router.push('/login')
}

const showPrivacy = () => {
  showPrivacyModal.value = true
}

const showTerms = () => {
  showTermsModal.value = true
}

const handleOpenFeedback = () => {
  showFeedbackModal.value = true
}

const handleFeedbackSuccess = () => {
  showFeedbackModal.value = false
  fetchBonusCredits()
}
</script>

<style scoped>
.app-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.nav-link-item {
  color: #666;
  text-decoration: none;
  font-size: 13px;
  transition: color 0.2s;
  padding: 6px 12px;
  border-radius: 6px;
}

.nav-link-item:hover {
  color: #4080FF;
  background: #f0f7ff;
}

.nav-link-item.active {
  color: #4080FF;
  font-weight: 500;
  background: #f0f7ff;
}

.nav-links .divider {
  color: #e8e8e8;
}

.top-nav {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 12px 0;
  background: white;
  border-bottom: 1px solid #e8e8e8;
  height: 56px;
  box-sizing: border-box;
}

.nav-container {
  width: 80%;
  max-width: 1200px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.nav-brand {
  display: flex;
  align-items: center;
  gap: 10px;
}

.brand-text {
  font-size: 16px;
  font-weight: 600;
  color: #333;
}

.nav-links {
  display: flex;
  align-items: center;
  gap: 8px;
}

.credits-display {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 6px 12px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 20px;
  color: white;
  font-size: 13px;
  font-weight: 500;
  margin-left: 12px;
}

.credits-text {
  white-space: nowrap;
}

.get-more-credits-btn {
  margin-left: 8px;
  padding: 4px 8px;
  background: rgba(255, 255, 255, 0.2);
  border: 1px solid rgba(255, 255, 255, 0.3);
  border-radius: 12px;
  color: white;
  font-size: 12px;
  cursor: pointer;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  gap: 4px;
}

.get-more-credits-btn:hover {
  background: rgba(255, 255, 255, 0.3);
}

.user-mobile {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 6px 12px;
  background: #f0f7ff;
  border-radius: 20px;
  color: #4080FF;
  font-size: 13px;
  font-weight: 500;
  margin-left: 12px;
}

.mobile-text {
  white-space: nowrap;
}

.logout-btn-small {
  background: none;
  border: none;
  color: #999;
  cursor: pointer;
  padding: 6px 12px;
  border-radius: 6px;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  font-size: 13px;
  margin-left: 12px;
}

.logout-btn-small:hover {
  background: #f5f7fa;
  color: #f56c6c;
}

.main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
}
</style>
