import Vue from 'vue'
import Router from 'vue-router'

// router components
import Home from '../pages/Home'
import Docs from '../pages/Docs'


Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'Home',
      component: Home
    },
    {
      path: '/Docs',
      name: 'Docs',
      component: Docs
    }
  ],
  linkActiveClass: 'is-active'
})
