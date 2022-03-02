import 'mdb-vue-ui-kit/css/mdb.min.css';
import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import http from './plugins/http';

createApp(App)
  .use(http)
  .use(router)
  .mount('#app');
