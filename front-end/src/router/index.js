import Vue from 'vue';
import VueRouter from 'vue-router';
import Index from '@/views/index/index.vue';
import About from '@/views/about/about.vue';
import Login from '@/views/login/login.vue';
import Register from '@/views/register/register.vue';
import UserInfo from '@/views/user-info/userInfo.vue';
import Message from '@/views/message/message.vue';
import Detail from '@/views/detail/detail.vue';

Vue.use(VueRouter);

const routes = [
  {
    path: '/index',
    name: 'Index',
    component: Index,
    alias: '/',
    meta: {
      keepAlive: true,
    },
  },
  {
    path: '/login',
    name: 'Login',
    component: Login,
  },
  {
    path: '/register',
    name: 'Register',
    component: Register,
  },
  {
    path: '/about',
    name: 'About',
    component: About,
  },
  {
    path: '/user-info',
    name: 'UserInfo',
    component: UserInfo,
  },
  {
    path: '/message',
    name: 'Message',
    component: Message,
  },
  {
    path: '/detail/:id',
    name: 'Detail',
    component: Detail,
  },
  {
    path: '/401',
    name: 'error401',
    component: () => import('@/views/error-page/401.vue'),
  },
  {
    path: '/500',
    name: 'error500',
    component: () => import('@/views/error-page/500.vue'),
  },
  {
    path: '*',
    name: 'error404',
    component: () => import('@/views/error-page/404.vue'),
  },
];

const router = new VueRouter({
  routes,
});

export default router;
