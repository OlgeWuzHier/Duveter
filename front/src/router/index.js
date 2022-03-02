import { createRouter, createWebHashHistory } from 'vue-router';
import Main from '../views/Main.vue';

// function isAuthenticated() {
//   return 1;
// }

const routes = [
  {
    path: '/',
    name: 'Main',
    component: Main,
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

// router.beforeEach((to, from, next) => {
//   if (to.name !== 'Login' && !isAuthenticated) next({ name: 'Login' });
//   else next();
// });

export default router;
