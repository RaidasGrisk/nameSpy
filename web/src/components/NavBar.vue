<template>
  <div>
    <nav class="navbar is-spaced is-transparent is-primary is-medium">
      <div class="container">
        <div class="navbar-brand">
          <a class="navbar-item" href="/">
            <img src="@/assets/white_large.png" alt="Logo">
          </a>
          <a class="navbar-item" href="/">
            <a href="https://github.com/RaidasGrisk/names_app" target="_blank" title="Github" class="navbar-item">
            <img src="@/assets/GitHub-Mark-Light-32px.png" alt="Logo">
            </a>
          </a>

          <div class="navbar-burger" @click="showNav = !showNav" :class="{ 'is-active': showNav }">
            <span></span>
            <span></span>
            <span></span>
          </div>
        </div>
        <div class="navbar-menu" :class="{ 'is-active': showNav }">
          <div class="navbar-end">
            <router-link class="navbar-item" v-for="routes in links"
            v-bind:key="routes.id"
            :to="`${routes.page}`">{{routes.text}}</router-link>
            <!-- Login button -->
            <!-- <button class="button is-normal is-success is-outlined"
            @click="showModal_Login=!showModal_Login">Login</button> -->
          </div>
        </div>
      </div>
    </nav>

    <!-- Keep all the modals at the bottom,
    else upon opening it the background shifts a little -->
    <Modal v-show="showModal_Login" @close="showModal_Login=false">
      <Login/>
    </Modal>
  </div>
</template>

<script>

import Login from '@/components/home/Login'
import Modal from '@/components/Modal'

export default {
  name: 'Navigation',

  components: {
    Login,
    Modal
  },

  data() {
    return {
      links: [
        {
          id: 0,
          text: 'Home',
          page: '/'
        },
        {
          id: 1,
          text: 'Docs',
          page: '/Docs'
        },
        // {
        //   id: 2,
        //   text: 'Contacts',
        //   page: '/Contacts'
        // }
      ],
      showNav: false,

      showModal_Login: false
    }
  }
}
</script>

<style scoped>

</style>
