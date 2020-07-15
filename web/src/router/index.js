import Vue from 'vue'
import Router from 'vue-router'

// router compontnts
import Home from '../components/LandingPage'
import Docs from '../components/Docs'


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
