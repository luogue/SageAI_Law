<template>
  <div class="admin-layout">
    <!-- 侧边栏 -->
    <aside class="sidebar">
      <div class="logo">
        <h1>SageAI</h1>
        <span>管理后台</span>
      </div>
      
      <el-menu 
        :default-active="activeMenu" 
        class="sidebar-menu"
        mode="vertical"
        @select="handleMenuSelect"
      >
        <el-menu-item index="/admin">
          <i class="el-icon-data-board"></i>
          <span>数据统计</span>
        </el-menu-item>
        <el-menu-item index="/admin/users">
          <i class="el-icon-user"></i>
          <span>用户管理</span>
        </el-menu-item>
        <el-menu-item index="/admin/feedbacks">
          <i class="el-icon-message"></i>
          <span>反馈审核</span>
        </el-menu-item>
        <el-menu-item index="/admin/blacklist">
          <i class="el-icon-ban"></i>
          <span>黑名单管理</span>
        </el-menu-item>
        <el-menu-item index="/admin/settings">
          <i class="el-icon-setting"></i>
          <span>系统设置</span>
        </el-menu-item>
        <el-menu-item index="/admin/usage">
          <i class="el-icon-document"></i>
          <span>使用记录</span>
        </el-menu-item>
      </el-menu>
    </aside>
    
    <!-- 主内容区 -->
    <main class="main-content">
      <!-- 顶部导航 -->
      <header class="top-header">
        <div class="header-left">
          <h2>{{ pageTitle }}</h2>
        </div>
        <div class="header-right">
          <span class="username">{{ username }}</span>
          <el-button type="text" @click="handleLogout">退出登录</el-button>
        </div>
      </header>
      
      <!-- 内容区域 -->
      <div class="content-wrapper">
        <router-view />
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'

const router = useRouter()
const route = useRoute()

const username = ref(localStorage.getItem('admin_username') || '管理员')

const activeMenu = computed(() => route.path)

const pageTitle = computed(() => {
    const titles = {
      '/admin': '数据统计',
      '/admin/users': '用户管理',
      '/admin/feedbacks': '反馈审核',
      '/admin/blacklist': '黑名单管理',
      '/admin/settings': '系统设置',
      '/admin/usage': '使用记录'
    }
    // 用户详情页特殊处理
    if (route.path.startsWith('/admin/users/')) {
      return '用户详情'
    }
    return titles[route.path] || '管理后台'
  })

function handleMenuSelect(index) {
  router.push(index)
}

function handleLogout() {
  localStorage.removeItem('admin_token')
  localStorage.removeItem('admin_username')
  router.push('/admin/login')
}
</script>

<style scoped>
.admin-layout {
  display: flex;
  min-height: 100vh;
  background: #f5f7fa;
}

.sidebar {
  width: 200px;
  background: #2f3542;
  color: white;
  display: flex;
  flex-direction: column;
}

.logo {
  padding: 20px;
  text-align: center;
  border-bottom: 1px solid #424854;
}

.logo h1 {
  font-size: 20px;
  margin: 0 0 4px 0;
  color: #667eea;
}

.logo span {
  font-size: 12px;
  color: #8a8f9a;
}

.sidebar-menu {
  flex: 1;
  border-right: none;
}

.sidebar-menu .el-menu-item {
  color: #b4bcc7;
  height: 48px;
  line-height: 48px;
}

.sidebar-menu .el-menu-item:hover,
.sidebar-menu .el-menu-item.is-active {
  background: #3a4049;
  color: white;
}

.main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.top-header {
  height: 60px;
  background: white;
  padding: 0 24px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
}

.header-left h2 {
  font-size: 18px;
  margin: 0;
  color: #303133;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 16px;
}

.username {
  font-size: 14px;
  color: #606266;
}

.content-wrapper {
  flex: 1;
  padding: 24px;
  overflow-y: auto;
}
</style>
