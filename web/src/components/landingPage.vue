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
        </div>

        <div class="field has-addons has-addons-centered">
          <p class="control">
            <a class="button is-small is-success is-inverted is-focused" @click="getModelApiData(job_title)">
              <div class="content is-small">
                Who is it?
              </div>
            </a>
          </p>
          <p class="control">
            <a class="button is-small is-info is-inverted is-focused" @click="getModelApiData(social_score)">
              <div class="content is-small">
                Web score?
              </div>
            </a>
          </p>
        </div>
      </div>
    </section>

    <section>
      <div class="columns is-centered">
        <div class="box" style="min-width: 30vh;" v-if="processingAPIRequest">
          <progress class="progress is-medium is-primary" max="100"></progress>
        </div>
        <!-- style="background-color: #0a131c;" -->
        <div class="box is-size-7" v-if="output">
          <vue-json-pretty
            :data="this.output"
            :showLine="false"
            :showDoubleQuotes="false">
          </vue-json-pretty>
        </div>
      </div>
    </section>

    <br><br>
    <section v-if="output">
      <div class="is-size-4 is-uppercase has-text-weight-bold has-text-centered">
        <p>Here, <br>have some perspective</p>
      </div>
      <SocialScoreBoard/>
    </section>

  </div>
</template>

<script>

import axios from "axios"
import VueJsonPretty from 'vue-json-pretty'

import SocialScoreBoard from './SocialScoreBoard'

export default {

  name: 'landingPage',

  components: {
    VueJsonPretty,
    SocialScoreBoard
  },

  data() {
    return {
      input: '',
      output: null,
      processingAPIRequest: false,

      // endpoints
      job_title: 'job_title',
      social_score: 'social_score'
    }
  },

  methods: {

    stringify(input) {
      return JSON.stringify(input, null, 4)
    },

    getModelApiData(endpoint) {

      this.output = null
      this.processingAPIRequest = true
      var vm = this
      var url = "http://127.0.0.1:5000/api/" + endpoint + "?input=" + this.input
      axios.get(url).then(function (response){
          vm.output = response.data
          vm.processingAPIRequest = false
        }
      )
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style>

.vjs-tree {
  font-size: 10px;
}

</style>
