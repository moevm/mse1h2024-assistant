import { createApp } from 'vue'
import App from './App.vue'

import router from '@/router'
import store from "@/store";

import axios from 'axios';

export const instance = axios.create({
    baseURL: 'http://localhost:5000',  // Установка базового URL
});

createApp(App).use(router).use(store).mount('#app')
