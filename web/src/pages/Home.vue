<template>
  <div class="section has-background-primary" style="margin-left: auto; margin-right: auto;">

    <transition name="fade" mode="out-in" appear>
      <div style="transition-delay: 1s">
        <Service/>
      </div>
    </transition>

  </div>
</template>

<script>


import Service from '@/components/home/Service'


export default {

  name: 'Home',

  components: {
    Service
  },

  data() {
    return {
    }
  },

  mounted() {

  }
}

</script>

<style>

.fade-enter-active, .fade-leave-active {
  transition: opacity 1s;
}
.fade-enter, .fade-leave-to /* .fade-leave-active below version 2.1.8 */ {
  opacity: 0;
}

</style>
