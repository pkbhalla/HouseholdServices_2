import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/components/HomeView.vue'
import AdminLogin from '@/components/AdminLogin.vue'
import AdminDashboard from '@/components/AdminDashboard.vue'
import LoginView from '@/components/LoginView.vue'
import CustomerRegister from '@/components/CustomerRegister.vue'
import ProfessionalRegister from '@/components/ProfessionalRegister.vue'
import CustomerDashboard from '@/components/CustomerDashboard.vue'
import ProfessionalDashboard from '@/components/ProfessionalDashboard.vue'
import AdminSummary from '@/components/AdminSummary.vue'
import CustomerSearch from '@/components/CustomerSearch.vue'


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/admin/login',
      name: 'adminlogin',
      component: AdminLogin,
    },
    {
      path: '/admin/dashboard',
      name: 'dashboard',
      component: AdminDashboard,
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView,
    },
    {
      path: '/register/customer',
      name: 'customer-register',
      component: CustomerRegister,
    },
    {
      path: '/register/professional',
      name: 'professional-register',
      component: ProfessionalRegister,
    },
    {
      path: '/customer/dashboard',
      name: 'customer-dashboard',
      component: CustomerDashboard,
    },
    {
      path: '/professional/dashboard',
      name: 'professional-dashboard',
      component: ProfessionalDashboard,
    },
    {
      path: '/admin/summary',
      name: 'admin-summary',
      component: AdminSummary,
    },
    {
      path: '/customer/search',
      name: 'customer-search',
      component: CustomerSearch,
    },
  ],
})

export default router
