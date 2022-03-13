import { createRouter, createWebHashHistory } from 'vue-router';
import isAuthenticated from '../helpers/isAuthenticated';

const routes = [
  {
    path: '/',
    name: 'Main',
    component: () => import('../views/Main.vue'),
  },
  {
    path: '/leaderboard',
    name: 'Leaderboard',
    // route level code-splitting
    // this generates a separate chunk (leaderboard.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "leaderboard" */ '../views/Leaderboard.vue'),
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('../views/Login.vue'),
  },
];

const router = createRouter({
  history: createWebHashHistory(),
  routes,
});

// Prevent unlogged access to anything but login
router.beforeEach((to) => {
  if (to.name !== 'Login' && !isAuthenticated()) {
    return { name: 'Login' };
  }
  return true;
});

// Prevent access to login page when logged
router.beforeEach((to) => {
  if (to.name === 'Login' && isAuthenticated()) {
    return { name: 'Main' };
  }
  return true;
});

export default router;
