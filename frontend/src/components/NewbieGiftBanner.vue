<template>
  <div class="newbie-banner" @click="handleClick">
    <div class="banner-content">
      <div class="gift-icon">🎁</div>
      <div class="banner-text">
        <span class="title">新手大礼包</span>
        <span class="desc">新用户注册即送3次免费审查额度，无使用期限</span>
      </div>
      <div class="arrow-icon">→</div>
    </div>
  </div>
</template>

<script setup>
const emit = defineEmits(['go-to-register'])

const handleClick = () => {
  emit('go-to-register')
}
</script>

<style scoped>
.newbie-banner {
  position: fixed;
  right: 20px;
  top: 50%;
  transform: translateY(-50%);
  background: linear-gradient(135deg, #ff6b6b 0%, #feca57 100%);
  border-radius: 12px;
  padding: 16px 20px;
  cursor: pointer;
  box-shadow: 0 8px 30px rgba(255, 107, 107, 0.4);
  z-index: 100;
  animation: bounce 2s infinite;
  transition: transform 0.2s, box-shadow 0.2s;
}

.newbie-banner:hover {
  transform: translateY(-50%) scale(1.05);
  box-shadow: 0 12px 40px rgba(255, 107, 107, 0.5);
}

.banner-content {
  display: flex;
  align-items: center;
  gap: 12px;
}

.gift-icon {
  font-size: 28px;
  animation: spin 3s linear infinite;
}

.banner-text {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.title {
  font-size: 14px;
  font-weight: 700;
  color: white;
}

.desc {
  font-size: 12px;
  color: rgba(255, 255, 255, 0.9);
  max-width: 140px;
}

.arrow-icon {
  font-size: 16px;
  color: white;
  font-weight: bold;
}

@keyframes bounce {
  0%, 100% {
    transform: translateY(-50%);
  }
  50% {
    transform: translateY(calc(-50% - 5px));
  }
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}
</style>
