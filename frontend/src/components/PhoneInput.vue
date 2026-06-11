<template>
  <div class="phone-input-container">
    <div class="phone-input-wrapper" :class="{ 'is-focus': isFocus, 'is-error': hasError }">
      <!-- 区号选择器 -->
      <div class="country-code-selector" @click.stop="toggleDropdown" ref="selectorRef">
        <span class="country-dial-code">{{ currentCountry.dialCode }}</span>
        <span class="dropdown-arrow" :class="{ 'is-open': showDropdown }">▼</span>
      </div>

      <!-- 区号下拉菜单 -->
      <Transition name="dropdown">
        <div 
          v-show="showDropdown" 
          class="country-dropdown" 
          ref="dropdownRef"
          :style="{ top: dropdownPosition.top + 'px', left: dropdownPosition.left + 'px' }"
        >
          <div class="dropdown-list">
            <div
              v-for="country in countryCodes"
              :key="country.code"
              class="dropdown-item"
              :class="{ 'is-active': country.code === currentCountry.code }"
              @click.stop="selectCountry(country)"
            >
              <span class="item-name">{{ country.name }}</span>
              <span class="item-dial-code">{{ country.dialCode }}</span>
            </div>
          </div>
        </div>
      </Transition>

      <!-- 手机号输入框 -->
      <input
        ref="phoneInputRef"
        :value="phoneNumber"
        type="tel"
        :placeholder="computedPlaceholder"
        :disabled="disabled"
        :maxlength="currentCountry.maxLength"
        @input="handleInput"
        @focus="isFocus = true"
        @blur="handleBlur"
        class="phone-number-input"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted, onBeforeUnmount, nextTick } from 'vue'
import { countryCodes, detectDefaultCountry, getCountryByCode } from '../constants/countryCodes.js'

const props = defineProps({
  modelValue: {
    type: String,
    default: ''
  },
  disabled: {
    type: Boolean,
    default: false
  },
  hasError: {
    type: Boolean,
    default: false
  },
  placeholder: {
    type: String,
    default: ''
  }
})

const emit = defineEmits(['update:modelValue', 'change', 'validate'])

const showDropdown = ref(false)
const isFocus = ref(false)
const selectorRef = ref(null)
const dropdownRef = ref(null)
const phoneInputRef = ref(null)
const dropdownPosition = ref({ top: 0, left: 0 })

const currentCountry = ref(getCountryByCode('CN'))
const phoneNumber = ref('')

// 计算占位符
const computedPlaceholder = computed(() => {
  return props.placeholder || currentCountry.value.placeholder || '请输入手机号'
})

const filteredCountries = computed(() => {
  return countryCodes
})

const fullPhoneNumber = computed(() => {
  const digits = phoneNumber.value.replace(/\D/g, '')
  if (!digits) return ''
  return currentCountry.value.dialCode + digits
})

// 校验手机号格式
function validatePhoneNumber(digits) {
  const country = currentCountry.value
  
  // 如果没有输入，返回 false
  if (!digits || digits.length === 0) {
    return { valid: false, message: '请输入手机号' }
  }
  
  // 使用国家的自定义校验函数
  if (country.validate) {
    const isValid = country.validate(digits)
    if (!isValid) {
      return { valid: false, message: '请输入有效的手机号' }
    }
  } else {
    // 默认校验：检查长度范围
    if (digits.length < country.minLength || digits.length > country.maxLength) {
      return { 
        valid: false, 
        message: `手机号长度应为 ${country.minLength}-${country.maxLength} 位` 
      }
    }
  }
  
  return { valid: true, message: '' }
}

onMounted(() => {
  const defaultCode = detectDefaultCountry()
  const country = getCountryByCode(defaultCode)
  if (country) {
    currentCountry.value = country
  }
  document.addEventListener('click', handleClickOutside)
})

onBeforeUnmount(() => {
  document.removeEventListener('click', handleClickOutside)
})

watch(() => props.modelValue, (val) => {
  if (!val || val === fullPhoneNumber.value) return
  for (const country of countryCodes) {
    if (val.startsWith(country.dialCode)) {
      currentCountry.value = country
      phoneNumber.value = val.slice(country.dialCode.length)
      return
    }
  }
  phoneNumber.value = val.replace(/\D/g, '')
}, { immediate: true })

function toggleDropdown() {
  if (props.disabled) return
  showDropdown.value = !showDropdown.value
  if (showDropdown.value) {
    nextTick(() => {
      const rect = selectorRef.value?.getBoundingClientRect()
      if (rect) {
        dropdownPosition.value = {
          top: rect.bottom + window.scrollY + 10,
          left: rect.left + window.scrollX
        }
      }
    })
  }
}

function selectCountry(country) {
  currentCountry.value = country
  // 切换国家时重置手机号
  phoneNumber.value = ''
  showDropdown.value = false
  emitValue()
  // 触发校验
  triggerValidation()
  nextTick(() => {
    phoneInputRef.value?.focus()
  })
}

function handleInput(e) {
  let val = e.target.value
  val = val.replace(/[^\d\s\-]/g, '')
  phoneNumber.value = val
  emitValue()
  // 实时校验
  triggerValidation()
}

function triggerValidation() {
  const digits = phoneNumber.value.replace(/\D/g, '')
  const result = validatePhoneNumber(digits)
  emit('validate', result)
}

function emitValue() {
  const full = fullPhoneNumber.value
  emit('update:modelValue', full)
  emit('change', {
    country: currentCountry.value,
    phoneNumber: phoneNumber.value,
    fullPhoneNumber: full
  })
}

function handleBlur() {
  isFocus.value = false
  // 失去焦点时触发校验
  triggerValidation()
}

function handleClickOutside(e) {
  if (showDropdown.value &&
      !selectorRef.value?.contains(e.target) &&
      !dropdownRef.value?.contains(e.target)) {
    showDropdown.value = false
  }
}

defineExpose({
  getFullPhoneNumber: () => fullPhoneNumber.value,
  getDigits: () => phoneNumber.value.replace(/\D/g, ''),
  validate: () => {
    const digits = phoneNumber.value.replace(/\D/g, '')
    const country = currentCountry.value
    return digits.length >= country.minLength && digits.length <= country.maxLength
  }
})
</script>

<style scoped>
.phone-input-container {
  width: 100%;
}

.phone-input-wrapper {
  width: 100%;
  height: 40px;
  display: flex;
  align-items: center;
  border: 1px solid #dcdfe6;
  border-radius: 8px;
  overflow: visible;
  background: #fff;
  transition: border-color 0.2s, box-shadow 0.2s;
  position: relative;
  box-sizing: border-box;
}

.phone-input-wrapper.is-focus {
  border-color: #4080ff;
  box-shadow: 0 0 0 2px rgba(64, 128, 255, 0.15);
}

.phone-input-wrapper.is-error {
  border-color: #ff6b6b;
}

.country-code-selector {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 0 12px;
  height: 100%;
  background: #f5f7fa;
  border-right: 1px solid #dcdfe6;
  cursor: pointer;
  user-select: none;
  flex-shrink: 0;
  transition: background 0.2s;
  border-top-left-radius: 7px;
  border-bottom-left-radius: 7px;
}

.country-code-selector:hover {
  background: #e4e7ed;
}

.country-dial-code {
  font-size: 14px;
  color: #606266;
  font-weight: 500;
  min-width: 40px;
}

.dropdown-arrow {
  font-size: 10px;
  color: #909399;
  transition: transform 0.2s;
}

.dropdown-arrow.is-open {
  transform: rotate(180deg);
}

.country-dropdown {
  position: fixed;
  width: 260px;
  max-height: 300px;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
  z-index: 9999;
  overflow-y: auto;
  border: 1px solid #e4e7ed;
}

.dropdown-list {
  padding: 4px 0;
}

.dropdown-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px 12px;
  cursor: pointer;
  transition: background 0.15s;
}

.dropdown-item:hover {
  background: #f5f7fa;
}

.dropdown-item.is-active {
  background: #ecf5ff;
  color: #4080ff;
}

.item-name {
  font-size: 14px;
  color: #303133;
}

.item-dial-code {
  font-size: 13px;
  color: #909399;
  font-weight: 500;
}

.dropdown-item.is-active .item-dial-code {
  color: #4080ff;
}

.dropdown-empty {
  padding: 20px;
  text-align: center;
  color: #909399;
  font-size: 14px;
}

.phone-number-input {
  flex: 1;
  height: 100%;
  padding: 0 12px;
  border: none;
  outline: none;
  font-size: 14px;
  color: #303133;
  background: transparent;
  min-width: 0;
  box-sizing: border-box;
}

.phone-number-input::placeholder {
  color: #c0c4cc;
}

.phone-number-input:disabled {
  background: #f5f7fa;
  cursor: not-allowed;
}

.dropdown-enter-active,
.dropdown-leave-active {
  transition: opacity 0.2s, transform 0.2s;
}

.dropdown-enter-from,
.dropdown-leave-to {
  opacity: 0;
  transform: translateY(-6px);
}

@media (max-width: 480px) {
  .country-dropdown {
    width: 240px;
    max-height: 280px;
  }

  .phone-number-input {
    font-size: 16px;
  }
}

@media (max-width: 360px) {
  .country-dropdown {
    width: calc(100vw - 40px);
    left: 50%;
    transform: translateX(-50%);
  }
}
</style>
