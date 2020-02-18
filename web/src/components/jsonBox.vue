<template>
  <div class="columns is-centered">
    <div class="box" style="min-width: 30vh;" v-if="processingAPIRequest">
      <progress class="progress is-medium is-primary" max="100"></progress>
    </div>
    <div class="box is-size-7" v-if="output">
      <vue-json-pretty
        :data=jsonData
        :showLine="false"
        :showDoubleQuotes="false">
      </vue-json-pretty>
    </div>
  </div>
</template>

<script>

import VueJsonPretty from 'vue-json-pretty'

export default {

  name: 'jsonBox',

  components: {
    VueJsonPretty
  },

  props: {
      jsonData: {
        type: JSON
      }
  },

  data() {
    return {
    }
  },

  methods: {

  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

</style>
