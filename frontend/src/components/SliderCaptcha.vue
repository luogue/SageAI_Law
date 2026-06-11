<template>
  <div class="captcha-modal" v-if="visible">
    <div class="captcha-container">
      <div class="captcha-header">
        <span>安全验证</span>
        <button class="close-btn" @click="handleClose">×</button>
      </div>
      <div class="captcha-body">
        <div class="captcha-img-container">
          <canvas ref="bgCanvas" width="320" height="160"></canvas>
          <canvas ref="sliderCanvas" width="320" height="160" class="slider-layer"></canvas>
          <div class="captcha-tip" v-if="tipMessage">{{ tipMessage }}</div>
        </div>
        <div class="slider-container">
          <div class="slider-track" :class="{ success: isSuccess, error: hasError }">
            <div class="slider-thumb" @mousedown="startDrag" @touchstart="startDrag">
              <div class="slider-arrow">→</div>
            </div>
            <div class="slider-gap" :style="{ left: gapPosition + 'px' }"></div>
          </div>
          <div class="slider-tip">{{ sliderTip }}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'

const props = defineProps({
  visible: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['success', 'close', 'error'])

const bgCanvas = ref(null)
const sliderCanvas = ref(null)
const isDragging = ref(false)
const startX = ref(0)
const currentX = ref(0)
const gapPosition = ref(0)
const tipMessage = ref('')
const hasError = ref(false)
const isSuccess = ref(false)
const sliderTip = ref('按住滑块，拖动到最右边完成验证')
const passWord = ref('')

const GAP_WIDTH = 40
const SLIDER_SIZE = 50

onMounted(() => {
  if (props.visible) {
    initCaptcha()
  }
})

watch(() => props.visible, (newVal) => {
  if (newVal) {
    setTimeout(() => initCaptcha(), 100)
  }
})

function initCaptcha() {
  isSuccess.value = false
  hasError.value = false
  tipMessage.value = ''
  sliderTip.value = '按住滑块，拖动到最右边完成验证'
  gapPosition.value = 0
  passWord.value = ''
  // 重置滑块位置
  currentX.value = 0
  if (sliderCanvas.value) {
    sliderCanvas.value.style.transform = ''
  }
  drawCaptcha()
}

function drawCaptcha() {
  const bgCtx = bgCanvas.value?.getContext('2d')
  const sliderCtx = sliderCanvas.value?.getContext('2d')
  if (!bgCtx || !sliderCtx) return

  // 清除画布
  bgCtx.clearRect(0, 0, 320, 160)
  sliderCtx.clearRect(0, 0, 320, 160)

  // 生成随机缺口位置（滑块需要拖动的距离）
  // 滑块初始位置在左侧，gapPosition 代表需要拖动的像素距离
  const targetDistance = Math.floor(Math.random() * (260 - 60)) + 60 // 60-260px 之间
  gapPosition.value = targetDistance

  // 绘制背景
  bgCtx.fillStyle = '#f0f0f0'
  bgCtx.fillRect(0, 0, 320, 160)

  // 绘制随机线条
  for (let i = 0; i < 5; i++) {
    bgCtx.strokeStyle = `rgba(${Math.random() * 255}, ${Math.random() * 255}, ${Math.random() * 255}, 0.3)`
    bgCtx.beginPath()
    bgCtx.moveTo(Math.random() * 320, Math.random() * 160)
    bgCtx.lineTo(Math.random() * 320, Math.random() * 160)
    bgCtx.stroke()
  }

  // 绘制干扰点
  for (let i = 0; i < 30; i++) {
    bgCtx.fillStyle = `rgba(${Math.random() * 255}, ${Math.random() * 255}, ${Math.random() * 255}, 0.5)`
    bgCtx.beginPath()
    bgCtx.arc(Math.random() * 320, Math.random() * 160, Math.random() * 3 + 1, 0, Math.PI * 2)
    bgCtx.fill()
  }

  // 在背景上绘制缺口形状（使用深色填充）
  // 缺口位置 = 滑块初始位置 (5px) + 拖动距离
  const gapX = 5 + targetDistance
  const gapY = Math.floor(Math.random() * 100) + 30
  bgCtx.fillStyle = '#e0e0e0'
  bgCtx.beginPath()
  bgCtx.roundRect(gapX, gapY, GAP_WIDTH, GAP_WIDTH, 8)
  bgCtx.fill()

  // 绘制滑块（在左侧 canvas 上）
  sliderCtx.fillStyle = '#fff'
  sliderCtx.shadowBlur = 3
  sliderCtx.shadowColor = 'rgba(0,0,0,0.2)'
  sliderCtx.beginPath()
  // 滑块初始位置在左侧
  sliderCtx.roundRect(5, gapY + 5, GAP_WIDTH - 10, GAP_WIDTH - 10, 5)
  sliderCtx.fill()

  // 绘制滑块边框
  sliderCtx.strokeStyle = '#ccc'
  sliderCtx.lineWidth = 1
  sliderCtx.stroke()
}

function startDrag(e) {
  if (isSuccess.value) return
  e.preventDefault()
  isDragging.value = true
  const clientX = e.type === 'touchstart' ? e.touches[0].clientX : e.clientX
  startX.value = clientX
  document.addEventListener('mousemove', onDrag)
  document.addEventListener('mouseup', endDrag)
  document.addEventListener('touchmove', onDrag)
  document.addEventListener('touchend', endDrag)
}

function onDrag(e) {
  if (!isDragging.value) return
  e.preventDefault()
  const clientX = e.type === 'touchmove' ? e.touches[0].clientX : e.clientX
  currentX.value = clientX - startX.value

  // 限制范围
  if (currentX.value < 0) currentX.value = 0
  if (currentX.value > 320 - SLIDER_SIZE) currentX.value = 320 - SLIDER_SIZE

  // 更新滑块位置
  const thumb = document.querySelector('.slider-thumb')
  if (thumb) {
    thumb.style.transform = `translateX(${currentX.value}px)`
  }

  // 同步移动 canvas 上的滑块图像
  if (sliderCanvas.value) {
    sliderCanvas.value.style.transform = `translateX(${currentX.value}px)`
  }
}

function endDrag() {
  if (!isDragging.value) return
  isDragging.value = false
  document.removeEventListener('mousemove', onDrag)
  document.removeEventListener('mouseup', endDrag)
  document.removeEventListener('touchmove', onDrag)
  document.removeEventListener('touchend', endDrag)

  // 验证结果
  const targetX = gapPosition.value
  const currentPos = currentX.value

  // 允许误差在5px以内
  if (Math.abs(currentPos - targetX) < 5) {
    // 验证成功
    isSuccess.value = true
    sliderTip.value = '验证成功！'
    tipMessage.value = ''

    // 滑到最右边
    const thumb = document.querySelector('.slider-thumb')
    if (thumb) {
      thumb.style.transform = `translateX(${280 - SLIDER_SIZE}px)`
    }

    setTimeout(() => {
      emit('success')
      handleClose()
    }, 500)
  } else {
    // 验证失败
    hasError.value = true
    sliderTip.value = '验证失败，请重试'
    tipMessage.value = '位置不正确'

    setTimeout(() => {
      hasError.value = false
      currentX.value = 0
      const thumb = document.querySelector('.slider-thumb')
      if (thumb) {
        thumb.style.transform = 'translateX(0px)'
      }
      drawCaptcha()
      sliderTip.value = '按住滑块，拖动到最右边完成验证'
      tipMessage.value = ''
    }, 1000)
  }
}

function handleClose() {
  emit('close')
  setTimeout(() => {
    initCaptcha()
  }, 300)
}
</script>

<style scoped>
.captcha-modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
}

.captcha-container {
  background: white;
  border-radius: 12px;
  width: 360px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
  overflow: hidden;
}

.captcha-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 20px;
  border-bottom: 1px solid #eee;
  font-weight: 600;
  color: #333;
}

.close-btn {
  background: none;
  border: none;
  font-size: 24px;
  color: #999;
  cursor: pointer;
  padding: 0;
  line-height: 1;
}

.close-btn:hover {
  color: #666;
}

.captcha-body {
  padding: 20px;
}

.captcha-img-container {
  position: relative;
  margin-bottom: 20px;
}

.captcha-img-container canvas {
  display: block;
  border-radius: 8px;
}

.slider-layer {
  position: absolute;
  top: 0;
  left: 0;
  cursor: pointer;
}

.captcha-tip {
  position: absolute;
  bottom: -25px;
  left: 0;
  right: 0;
  text-align: center;
  font-size: 12px;
  color: #f56c6c;
}

.slider-container {
  margin-top: 40px;
}

.slider-track {
  position: relative;
  height: 50px;
  background: #f5f5f5;
  border-radius: 25px;
  border: 2px solid #e0e0e0;
  overflow: hidden;
}

.slider-track.success {
  border-color: #67c23a;
  background: #f0f9eb;
}

.slider-track.error {
  border-color: #f56c6c;
  background: #fef0f0;
}

.slider-thumb {
  position: absolute;
  top: 0;
  left: 0;
  width: 50px;
  height: 46px;
  background: #fff;
  border-radius: 50%;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
  cursor: grab;
  display: flex;
  align-items: center;
  justify-content: center;
  user-select: none;
  transition: transform 0.1s;
}

.slider-thumb:active {
  cursor: grabbing;
}

.slider-arrow {
  font-size: 18px;
  color: #666;
}

.slider-gap {
  position: absolute;
  top: 0;
  width: 40px;
  height: 46px;
  background: #fff;
  border-radius: 8px;
  opacity: 0;
}

.slider-tip {
  text-align: center;
  margin-top: 15px;
  font-size: 13px;
  color: #999;
}
</style>
