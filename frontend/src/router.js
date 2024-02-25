import { createRouter, createWebHashHistory } from 'vue-router'
import Login from "@/components/Login.vue";
import Chat from "@/components/Chat.vue";

const routes = [
    { path: '/', name: 'Login', component: Login },
    { path: '/chat', name: 'Chat', component: Chat },
]
const router = createRouter({
    history: createWebHashHistory(),
    routes
})
export default router