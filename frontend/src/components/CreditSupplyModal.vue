<template>
  <div v-if="visible" class="modal-overlay" @click="handleClose">
    <div class="modal-container" @click.stop>
      <div class="modal-header">
        <div class="header-icon">🎁</div>
        <h2>额度补给站</h2>
        <button class="close-btn" @click="handleClose">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <line x1="18" y1="6" x2="6" y2="18"></line>
            <line x1="6" y1="6" x2="18" y2="18"></line>
          </svg>
        </button>
      </div>
      
      <div class="modal-body">
        <div class="supply-items">
          <!-- 反馈有礼 -->
          <div class="supply-item">
            <div class="item-icon feedback">✓</div>
            <div class="item-content">
              <h3>反馈有礼</h3>
              <p>提交高质量反馈，审核通过后额外赠送3次额度</p>
            </div>
            <button class="item-btn" @click="handleFeedback">立即参与</button>
          </div>
          
          <!-- 邀请有礼 -->
          <div class="supply-item">
            <div class="item-icon invite">✓</div>
            <div class="item-content">
              <h3>邀请有礼</h3>
              <p>邀请好友注册，好友首次成功审查合同后，您和好友各得3次额度</p>
            </div>
            <button class="item-btn" @click="handleInvite">分享邀请</button>
          </div>
          
          <!-- 新品尝鲜 -->
          <div class="supply-item">
            <div class="item-icon taste">✓</div>
            <div class="item-content">
              <h3>新品尝鲜</h3>
              <p>帮助我们测试新功能，不定期赠送额度</p>
            </div>
            <button class="item-btn" @click="handleTaste">了解详情</button>
          </div>
        </div>
        
        <div class="disclaimer">
          <span>*本活动最终解释权归明月AI所有</span>
        </div>
      </div>
      
      <div class="modal-footer">
        <button class="close-modal-btn" @click="handleClose">关闭</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ElMessage } from 'element-plus'
import { useRouter } from 'vue-router'

const router = useRouter()

defineProps({
  visible: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['close', 'open-feedback'])

const handleClose = () => {
  emit('close')
}

const handleFeedback = () => {
  // 跳转到我的报告页面
  router.push('/reports')
  emit('close')
}

const handleInvite = async () => {
  // 从localStorage获取用户ID
  const userId = localStorage.getItem('user_id')
  if (!userId) {
    ElMessage.warning('请先登录')
    return
  }
  
  // 生成邀请链接（使用当前访问的域名，兼容各种部署环境）
  const baseUrl = window.location.origin
  const inviteLink = `${baseUrl}/register?inviter_id=${userId}`
  
  // 复制到剪贴板的三重兜底方案：
  // 1. Clipboard API（现代浏览器 + HTTPS）
  // 2. execCommand（旧浏览器 / HTTP 环境）
  // 3. 直接展示链接让用户手动复制
  let copied = false
  
  // 方案1：Clipboard API
  if (navigator.clipboard && typeof navigator.clipboard.writeText === 'function') {
    try {
      await navigator.clipboard.writeText(inviteLink)
      copied = true
    } catch (e) {
      console.warn('Clipboard API 写入失败，尝试 fallback:', e.message)
    }
  }
  
  // 方案2：execCommand 兜底（适用于 HTTP 环境）
  if (!copied) {
    try {
      const textarea = document.createElement('textarea')
      textarea.value = inviteLink
      textarea.style.position = 'fixed'
      textarea.style.left = '-9999px'
      textarea.style.top = '-9999px'
      // 确保 textarea 可读可写，避免 iOS 等平台的限制
      textarea.setAttribute('readonly', '')
      document.body.appendChild(textarea)
      textarea.focus()
      textarea.select()
      // iOS 需要特殊处理 selection range
      if (navigator.userAgent.match(/ipad|iphone/i)) {
        textarea.setSelectionRange(0, inviteLink.length)
      }
      const successful = document.execCommand('copy')
      document.body.removeChild(textarea)
      if (successful) {
        copied = true
      }
    } catch (err) {
      console.warn('execCommand 兜底方案也失败:', err.message)
    }
  }
  
  if (copied) {
    ElMessage.success('邀请链接已复制到剪贴板！')
  } else {
    // 方案3：无法自动复制时，直接展示链接供用户手动复制
    console.error('所有剪贴板方案均失败，展示链接供手动复制')
    ElMessage({
      message: `邀请链接: ${inviteLink}\n（已为您选中，可直接复制）`,
      type: 'info',
      duration: 5000,
      showClose: true
    })
    // 尝试选中文本便于用户 Ctrl+C
    try {
      const tempDiv = document.createElement('div')
      tempDiv.textContent = inviteLink
      tempDiv.style.position = 'fixed'
      tempDiv.style.left = '0'
      tempDiv.style.right = '0'
      tempDiv.style.bottom = '60px'
      tempDiv.style.padding = '12px 20px'
      tempDiv.style.background = '#323232'
      tempDiv.style.color = '#fff'
      tempDiv.style.fontSize = '13px'
      tempDiv.style.textAlign = 'center'
      tempDiv.style.zIndex = '10000'
      tempDiv.style.cursor = 'pointer'
      tempDiv.style.wordBreak = 'break-all'
      tempDiv.title = '点击复制'
      tempDiv.addEventListener('click', () => {
        navigator.clipboard?.writeText(inviteLink)
        ElMessage.success('已复制！')
        document.body.removeChild(tempDiv)
      })
      document.body.appendChild(tempDiv)
      setTimeout(() => {
        if (tempDiv.parentNode) {
          document.body.removeChild(tempDiv)
        }
      }, 8000)
    } catch (_) { /* 忽略 */ }
  }
}

const handleTaste = () => {
  ElMessage.info('新功能即将上线，敬请期待！')
}
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-container {
  background: white;
  border-radius: 16px;
  width: 90%;
  max-width: 500px;
  overflow: hidden;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.2);
}

.modal-header {
  display: flex;
  align-items: center;
  padding: 20px 24px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.header-icon {
  font-size: 28px;
  margin-right: 12px;
}

.modal-header h2 {
  flex: 1;
  margin: 0;
  font-size: 18px;
  font-weight: 600;
}

.close-btn {
  background: none;
  border: none;
  color: white;
  cursor: pointer;
  padding: 4px;
}

.modal-body {
  padding: 24px;
}

.supply-items {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.supply-item {
  display: flex;
  align-items: center;
  padding: 16px;
  background: #f8f9fa;
  border-radius: 12px;
  gap: 16px;
}

.item-icon {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: bold;
  font-size: 16px;
}

.item-icon.feedback {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.item-icon.invite {
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
}

.item-icon.taste {
  background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
}

.item-content {
  flex: 1;
}

.item-content h3 {
  margin: 0 0 4px 0;
  font-size: 15px;
  font-weight: 600;
  color: #333;
}

.item-content p {
  margin: 0;
  font-size: 13px;
  color: #666;
}

.item-btn {
  padding: 8px 16px;
  background: white;
  border: 1px solid #4080FF;
  border-radius: 20px;
  color: #4080FF;
  font-size: 13px;
  cursor: pointer;
  transition: all 0.2s;
}

.item-btn:hover {
  background: #4080FF;
  color: white;
}

.disclaimer {
  margin-top: 20px;
  text-align: center;
  font-size: 12px;
  color: #999;
}

.modal-footer {
  padding: 16px 24px;
  border-top: 1px solid #eee;
  display: flex;
  justify-content: center;
}

.close-modal-btn {
  padding: 10px 40px;
  background: #4080FF;
  border: none;
  border-radius: 25px;
  color: white;
  font-size: 14px;
  cursor: pointer;
  transition: background 0.2s;
}

.close-modal-btn:hover {
  background: #3070EF;
}
</style>
