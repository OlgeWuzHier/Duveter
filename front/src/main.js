import 'mdb-vue-ui-kit/css/mdb.min.css';
import { createApp } from 'vue';
import { io } from 'socket.io-client';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import App from './App.vue';
import router from './router';
import jwtInterceptor from './interceptors/jwtInterceptor';

jwtInterceptor();

createApp(App)
  .provide('socket', io('https://duveter-back.azurewebsites.net'))
  .use(router)
  .component('font-awesome-icon', FontAwesomeIcon)
  .mount('#app');
