import { createRouter, createWebHistory } from 'vue-router'

// 路由守卫：检查管理员登录状态
function requireAuth(to, from, next) {
  const token = localStorage.getItem('admin_token')
  if (token) {
    next()
  } else {
    next('/admin/login')
  }
}

const routes = [
  {
    path: '/admin/login',
    name: 'AdminLogin',
    component: () => import('../views/admin/Login.vue')
  },
  {
    path: '/admin',
    name: 'Admin',
    component: () => import('../views/admin/AdminLayout.vue'),
    beforeEnter: requireAuth,
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
