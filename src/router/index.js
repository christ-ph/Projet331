import { createRouter, createWebHistory } from 'vue-router';
import HomeView from '../views/HomeView.vue';
import LoginView from '../views/LoginView.vue';
import RegisterView from '../views/RegisterView.vue';
import DashboardView from '../views/DashboardView.vue';
import UserProfileView from '../views/UserProfileView.vue';
import FreelanceProfileView from '../views/FreelanceProfileView.vue';
import MissionsView from '../views/MissionsView.vue';
import DashbordViewClient from '@/views/DashbordViewClient.vue';
import MissionsViewClient from '@/views/MissionsViewClient.vue';
import MissionApplicationsView from '@/views/MissionApplicationsView.vue';

const routes = [
  { 
    path: '/', 
    name: "Home", 
    component: HomeView,
    props: true
  },
  { 
    path: '/login', 
    name: "Login", 
    component: LoginView,
    props: true
  },
  { 
    path: '/register', 
    name: "Register", 
    component: RegisterView,
    props: true
  },
  { 
    path: '/dashboard', 
    name: "Dashboard", 
    component: DashboardView, 
    meta: { requiresAuth: true },
    props: true
  },
  { 
    path: '/profile', 
    name: "Profile", 
    component: UserProfileView, 
    meta: { requiresAuth: true },
    props: true
  },
  { 
    path: '/freelance-profile', 
    name: "FreelanceProfile", 
    component: FreelanceProfileView, 
    meta: { requiresAuth: true },
    props: true
  },
  { 
    path: '/missions', 
    name: "Missions", 
    component: MissionsView, 
    meta: { requiresAuth: true },
    props: true
  },
   { 
    path: '/missions-client', 
    name: "Missions-client", 
    component: MissionsViewClient, 
    meta: { requiresAuth: true },
    props: true
  },
   { 
    path: '/dashboard-client', 
    name: "Dashboard-client", 
    component: DashbordViewClient, 
    meta: { requiresAuth: true },
    props: true
  },
  {
    path: '/missionsApplications',
    name: "MissionApplicationsView",
    component: MissionApplicationsView,
    meta: { requiresAuth: true },
    props: true
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

// Garde de route pour l'authentification
router.beforeEach((to, from, next) => {
  const user = JSON.parse(localStorage.getItem('user'));
  if (to.meta.requiresAuth && !user) {
    next('/login');
  } else {
    next();
  }
});

export default router;