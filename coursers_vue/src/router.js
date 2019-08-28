import Vue from 'vue'
import Router from 'vue-router'
import Home from './views/Home.vue'

Vue.use(Router)

export default new Router({
    routes: [
        {
            path: '/',
            name: 'home',
            component: Home
        },
        {
            path: '/checkinsystem',
            name: 'checkinsystem',
            component: () => import('./views/CheckInSystem.vue')
        },
        {
            path: '/friendlylink',
            name: 'friendlylink',
            component: () => import('./views/FriendlyLink.vue')
        },
        {
            path: '/userhome',
            name: 'userhome',
            component: () => import('./views/UserHome.vue')
        },
        {
            path: '/admin',
            name: 'admin',
            component: () => import('./views/Admin.vue')
        }
    ]
})
