<template>
  <div class="has-text-white-ter">

    <section class="section">

      <div class="columns is-one-fifth is-centered">
        <div class="box has-text-centered">
          <img src="@/assets/Picture1.png" alt="Logo" style="width:100px;">
        </div>
      </div>

      <div class="has-text-centered">
        <div class="section">
          <div class="is-size-4 is-uppercase has-text-weight-bold">
            Hi, my names is
          </div>
          <div class="is-size-4 is-uppercase has-text-weight-bold has-text-success">
            NameSpy
        </div>
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
      <SocialScoreBoard :gridData="getGridData()"></SocialScoreBoard>
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
      social_score: 'social_score',

      // table data
      gridData: [
        {'person': 'Albert Einstein', 'google_items': 62800000, 'wiki_items': 4511, 'twtr_users': 20, 'twtr_followers': 143596, 'ig_users': 31, 'ig_followers': 810100},
        {'person': 'Nicki Minaj', 'google_items': 115000000, 'wiki_items': 2800, 'twtr_users': 20, 'twtr_followers': 20602384, 'ig_users': 27, 'ig_followers': 623500},
        {'person': 'Charles Darwin', 'google_items': 14500000, 'wiki_items': 3936, 'twtr_users': 20, 'twtr_followers': 2875083, 'ig_users': 26, 'ig_followers': 506},
        {'person': 'Elon Musk', 'google_items': 91000000, 'wiki_items': 838, 'twtr_users': 20, 'twtr_followers': 31396013, 'ig_users': 16, 'ig_followers': 6383},
        {'person': 'Bart Simpson', 'google_items': 12900000, 'wiki_items': 432, 'twtr_users': 20, 'twtr_followers': 46045, 'ig_users': 21, 'ig_followers': 25700},
        {'person': 'Karolina Meschino', 'google_items': 695000, 'wiki_items': 4, 'twtr_users': 1, 'twtr_followers': 132, 'ig_users': 41, 'ig_followers': 289300},
        // {'person': 'Guido van Rossum', 'google_items': 478000, 'wiki_items': 98, 'twtr_users': 3, 'twtr_followers': 168370, 'ig_users': 3, 'ig_followers': 951},
        // {'person': 'Evan You', 'google_items': 212000, 'wiki_items': 2, 'twtr_users': 20, 'twtr_followers': 99680, 'ig_users': 42, 'ig_followers': 4148},
        // {'person': 'Agnė Širinskienė', 'google_items': 171000, 'wiki_items': 3, 'twtr_users': 0, 'twtr_followers': 0, 'ig_users': 0, 'ig_followers': 0},
        // {'person': 'Karolina Zivkovic', 'google_items': 225, 'wiki_items': 0, 'twtr_users': 1, 'twtr_followers': 0, 'ig_users': 10, 'ig_followers': 171},
        // {'person': 'Oleksii Potiekhin', 'google_items': 13200, 'wiki_items': 0, 'twtr_users': 1, 'twtr_followers': 3, 'ig_users': 0, 'ig_followers': 0}
      ]
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
      var url = "http://127.0.0.1:8080/api/" + endpoint + "?input=" + this.input
      axios.get(url).then(function (response){
          vm.output = response.data
          vm.processingAPIRequest = false
        }
      )
    },

    checkIfArrayIsEmpty(array, index) {
      if (array.length == 0) {
        return {'followers_count': 0}
      } else {
        return array[index]
      }
    },

    getGridData() {
      if (
        (this.output !== 'undefined') &&
        (this.output != null) &&
        ('input' in this.output) &&
        (this.output['input'] != this.gridData[this.gridData.length-1]['person'])
      ) {
        // map API data to gridData table
        var newRow = {
          'person': this.output['input'],
          'google_items': this.output['google']['items'],
          'wiki_items': this.output['wikipedia']['items'],
          'twtr_users': this.output['twitter']['num_users'],
          'twtr_followers': this.checkIfArrayIsEmpty(this.output['twitter']['users'], 0)['followers_count'],
          'ig_users': this.output['instagram']['num_users'],
          'ig_followers': this.checkIfArrayIsEmpty(this.output['instagram']['users'], 0)['followers_count'],
          'class': 'is-success'
        }
        this.gridData.push(newRow)
      }
      return this.gridData
    }
  },

}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style>

.vjs-tree {
  font-size: 10px;
}

</style>
