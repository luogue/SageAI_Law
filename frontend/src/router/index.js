import { createRouter, createWebHistory } from 'vue-router'

// 路由守卫：检查用户登录状态
function requireAuth(to, from, next) {
  const token = localStorage.getItem('token')
  if (token) {
    next()
  } else {
    next('/login')
  }
}

// 路由守卫：已登录用户访问登录页自动跳转首页
function redirectIfLoggedIn(to, from, next) {
  const token = localStorage.getItem('token')
  if (token) {
    next('/')
  } else {
    next()
  }
}

// 管理员路由守卫
function requireAdminAuth(to, from, next) {
  const adminToken = localStorage.getItem('admin_token')
  if (adminToken) {
    next()
  } else {
    next('/admin/login')
  }
}

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('../views/Login.vue'),
    beforeEnter: redirectIfLoggedIn
  },
  {
    path: '/',
    name: 'Home',
    component: () => import('../views/Home.vue'),
    beforeEnter: requireAuth,
    children: [
      {
        path: '',
        name: 'Upload',
        component: () => import('../components/UploadPage.vue'),
        meta: { keepAlive: true }
      },
      {
        path: 'reports',
        name: 'Reports',
        component: () => import('../components/MyReports.vue')
      },
      {
        path: 'report/:id',
        name: 'ReportDetail',
        component: () => import('../components/ResultPage.vue')
      },
      {
        path: 'adjudicate',
        name: 'AdjudicateDeposit',
        component: () => import('../views/AdjudicateDeposit.vue')
      },
      {
        path: 'adjudicate-v2',
        name: 'AdjudicateDepositV2',
        component: () => import('../views/AdjudicateDepositV2.vue')
      }
    ]
  },
  // ========== 后台管理路由 ==========
  {
    path: '/admin/login',
    name: 'AdminLogin',
    component: () => import('../views/admin/Login.vue')
  },
  {
    path: '/admin',
    name: 'Admin',
    component: () => import('../views/admin/AdminLayout.vue'),
    beforeEnter: requireAdminAuth,
    children: [
      {
        path: '',
        name: 'AdminDashboard',
        component: () => import('../views/admin/Dashboard.vue')
      },
      {
        path: 'users',
        name: 'UserList',
        component: () => import('../views/admin/UserList.vue')
      },
      {
        path: 'users/:id',
        name: 'UserDetail',
        component: () => import('../views/admin/UserDetail.vue')
      },
      {
        path: 'feedbacks',
        name: 'FeedbackList',
        component: () => import('../views/admin/FeedbackList.vue')
      },
      {
        path: 'blacklist',
        name: 'Blacklist',
        component: () => import('../views/admin/Blacklist.vue')
      },
      {
        path: 'settings',
        name: 'Settings',
        component: () => import('../views/admin/Settings.vue')
      },
      {
        path: 'usage',
        name: 'Usage',
        component: () => import('../views/admin/Usage.vue')
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
