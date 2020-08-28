<template>
  <div>
    <div class="columns is-one-fifth is-centered">
      <div class="modal is-active">
        <div class="modal-background"></div>
        <div class="modal-content">

          <ExplainCardOccupation/>

        </div>
        <button class="modal-close is-large" @click="$emit('close')"></button>
      </div>
    </div>
  </div>
</template>

<script>

import ExplainCardOccupation from './ExplainCardOccupation'

export default {

  name: 'ExplainCardOccupationModal',

  components: {
    ExplainCardOccupation
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
      });
  },

}
</script>


<style scoped>

</style>
