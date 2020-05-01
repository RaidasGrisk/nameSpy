<template>
  <nav class="navbar is-spaced has-shadow is-primary is-transparent">
    <div class="navbar-brand">
      <a class="navbar-item" href="/">
        <img src="@/assets/Picture3.png" alt="Logo">
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
      </div>
    </div>
  </nav>
</template>

<script>
export default {
  name: 'Navigation',
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
      showNav: false
    }
  }
}
</script>
