<template>
  <div>
    <div class="columns is-one-fifth is-centered">
      <div class="modal is-active">
        <div class="modal-background"></div>
        <div class="modal-content">

          <ExplainCardWebScore/>

        </div>
        <button class="modal-close is-large" @click="$emit('close')"></button>
      </div>
    </div>
  </div>
</template>

<script>

import ExplainCardWebScore from './ExplainCardWebScore'

export default {

  name: 'ExplainCardWebScoreModal',

  components: {
    ExplainCardWebScore
  },

  props: {
  },

  data() {
    return {
    }
  },

  computed: {
  },

  methods: {
  },

  mounted() {
      // Close modal with 'esc' key
      document.addEventListener("keydown", (e) => {
          if (e.keyCode == 27) {
              this.$emit('close');
          }
      })
  },

}
</script>


<style scoped>

</style>
