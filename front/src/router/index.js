import { createRouter, createWebHashHistory } from 'vue-router';
import isAuthenticated from '../helpers/isAuthenticated';

const routes = [
  {
    path: '/',
    name: 'Lobby',
    component: () => import('../views/Lobby.vue'),
  },
  {
    path: '/leaderboard',
    name: 'Leaderboard',
    component: () => import('../views/Leaderboard.vue'),
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('../views/Login.vue'),
  },
  {
    path: '/game/:id',
    name: 'Game',
    component: () => import('../views/Game.vue'),
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
    return { name: 'Lobby' };
  }
  return true;
});

export default router;
