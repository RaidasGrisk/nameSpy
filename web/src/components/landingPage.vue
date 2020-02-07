<template>
  <div class="has-text-white-ter">

    <section class="section">

      <div class="columns is-one-fifth is-centered">
        <div class="box has-text-centered">
          <img src="@/assets/Picture1.png" alt="Logo" style="width:100px;">
        </div>
      </div>

      <div class="has-text-centered">
        <div class="section is-size-4 is-uppercase has-text-weight-bold">
          Hi, my names is names.ml
        </div>

        <!-- <div class="content"> -->
          <div class="is-size-4 is-uppercase has-text-weight-bold">
            <p>What I do?</p>
          </div>

          <div class="content is-size-7">
            <p>You give me a name <br>
            I give you what I know about it.</p>
          </div>

          <div class="is-size-4 is-uppercase has-text-weight-bold">
            <p>Enough talk, simply try me.</p>
          </div>

          <div class="content is-size-7">
            <p>Type any name  and see what's up.<br>How about your own name?</p>
          </div>
        <!-- </div> -->

        <div class="field has-addons has-addons-centered">
          <p class="control">
            <input class="input is-small" v-model='input' type="text" placeholder="e.g. Rick Morty">
          </p>
          <p class="control">
            <a class="button is-small" @click="getModelApiData()">
              <div class="content is-small">
                Hit me!
              </div>
            </a>
          </p>
        </div>
      </div>
    </section>

    <div class="columns is-centered">
      <div class="box" style="min-width: 30vh;" v-if="processingAPIRequest">
        <progress class="progress is-medium is-primary" max="100"></progress>
      </div>
      <div class="box is-size-7" v-if="output">
        <pre>{{ stringify(this.output) }}</pre>
      </div>
    </div>

  </div>
</template>

<script>

import axios from "axios"

export default {

  name: 'landingPage',

  data() {
    return {
      input: '',
      output: null,
      processingAPIRequest: false
    }
  },

  methods: {

    stringify(input) {
      return JSON.stringify(input, null, 4)
    },

    getModelApiData() {

      this.output = null
      this.processingAPIRequest = true
      var vm = this
      var endpoint = "http://127.0.0.1:5000/api?input=" + this.input
      axios.get(endpoint).then(function (response){
          vm.output = response.data
          vm.processingAPIRequest = false
        }
      )
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

</style>
