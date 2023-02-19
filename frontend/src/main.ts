import { createApp } from 'vue'
import Antd from 'ant-design-vue';
import App from './App.vue'
import axios from 'axios'
import 'ant-design-vue/dist/antd.css';

const app = createApp(App)
app.config.globalProperties.$http = axios
app.use(Antd).mount('#app');
