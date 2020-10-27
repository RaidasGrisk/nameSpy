<template>
  <div id="app">
    <NavBar v-if="renderHero"/>
    <Hero v-if="!renderHero"/>
    <router-view/>
    <Footer/>
  </div>
</template>

<script>

import NavBar from './components/NavBar.vue'
import Footer from './components/Footer.vue'
import Hero from './components/home/Hero.vue'

export default {
  name: 'app',
  components: {
    NavBar,
    Hero,
    Footer
  },

  computed: {
    // hero component already has a navbar component
    // (must be this way so that navbar can be on top of hero)
    // therefore on some pages we want to alternate between rendering
    // navbar and hero components
    renderHero: function () {
      return this.$route.name != 'Home'
    }
  }

}
</script>

<style lang="scss">

// Import Bulma's core
@import "~bulma/sass/utilities/_all";

// Set your colors
// https://coolors.co/ffbe0b-fb5607-ff006e-8338ec-3a86ff
$primary: #8338EC;
$success: #FFBE0B;
$info: #3A86FF;
$warning: #FFBE0B;
$danger: #FB5607;
$primary-invert: findColorInvert($primary);

// Setup $colors to use as bulma classes (e.g. 'is-twitter')
$colors: (
    "white": ($white, $black),
    "black": ($black, $white),
    "light": ($light, $light-invert),
    "dark": ($dark, $dark-invert),
    "primary": ($primary, $primary-invert),
    "info": ($info, $info-invert),
    "success": ($success, $success-invert),
    "warning": ($warning, $warning-invert),
    "danger": ($danger, $danger-invert)
);

// Links
$link: $danger;
$link-invert: $primary-invert;
$link-focus-border: $primary;

// Import Bulma and Buefy styles
@import "~bulma";
@import url('https://fonts.googleapis.com/css?family=Roboto+Condensed');

#app {

  /* init */
  font-family: 'B616', sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  background-color: $primary;

}
</style>
