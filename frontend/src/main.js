import { createApp } from 'vue'
import App from './App.vue'
// Vuetify
// import 'vuetify/lib/styles/main.css'
// import "@mdi/font/css/materialdesignicons.css";
// import { createVuetify } from 'vuetify'
// import * as components from 'vuetify/components'
// import * as directives from 'vuetify/directives'

import router from '@/router'
import store from "@/store";

import axios from 'axios';

export const instance = axios.create({
    baseURL: 'http://localhost:5000',  // Установка базового URL
});

// const vuetify = createVuetify({
//   components,
//   directives,
// })

//createApp(App).use(vuetify).use(router).use(store).mount('#app')
createApp(App).use(router).use(store).mount('#app')
