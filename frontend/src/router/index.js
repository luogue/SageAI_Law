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

// 路由守卫：已登录用户访问登录/注册页自动跳转首页
function redirectIfLoggedIn(to, from, next) {
  const token = localStorage.getItem('token')
  if (token) {
    next('/')
  } else {
    next()
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
    path: '/register',
    name: 'Register',
    component: () => import('../views/Register.vue'),
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
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
