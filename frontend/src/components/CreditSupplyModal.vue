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
