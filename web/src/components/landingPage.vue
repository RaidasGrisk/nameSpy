<template>
  <div>
    <section class="section has-text-centered has-text-white-ter">

      <transition name="fade" mode="out-in" appear>
        <div class="columns is-one-fifth is-centered" style="transition-delay: 0.3s">
          <div class="box has-text-centered">
            <img src="@/assets/Picture1.png" alt="Logo" style="width:100px;">
          </div>
        </div>
      </transition>


      <transition name="fade" mode="out-in" appear>
        <div class="section"  style="transition-delay: 0.6s">
          <div class="is-size-4 is-uppercase has-text-weight-bold">
            Hi, my names is
          </div>
          <div class="is-size-4 is-uppercase has-text-weight-bold has-text-success">
            NameSpy <br> 🧐
          </div>
        </div>
      </transition>

        <!-- <div class="content"> -->
        <transition name="fade" mode="out-in" appear>
          <div class="section" style="transition-delay: 1.2s">
            <div class="is-size-4 is-uppercase has-text-weight-bold">
              <p>What I do?</p>
            </div>
            <div class="content is-size-7"  style="transition-delay: 0.9s">
              <p>You give me a name <br>
              I give you what I know about it.</p>
            </div>
          </div>
        </transition>


        <transition name="fade" mode="out-in" appear>
          <div class="section" style="transition-delay: 1.8s">
            <div class="is-size-4 is-uppercase has-text-weight-bold">
              <p>Enough talk, <br>try me</p>
            </div>

            <div class="content is-size-7">
              <p>Read the DOCS or <br>type in a name and see what's up</p>
            </div>

            <div class="field has-addons has-addons-centered">
              <p class="control">
                <input class="input is-small" v-model='input' type="text" placeholder="">
              </p>
            </div>

            <div class="field has-addons has-addons-centered">
              <p class="control">
                <a class="button is-small is-info is-inverted is-focused" @click="getModelApiData(social_score)">
                  <div class="content is-small">
                    web score
                  </div>
                </a>
              </p>
              <p class="control">
                <a class="button is-small is-success is-inverted is-focused" @click="getModelApiData(job_title)">
                  <div class="content is-small">
                    occupation
                  </div>
                </a>
              </p>
            </div>
          </div>
        </transition>

    </section>


    <section>
      <div class="columns is-centered">
        <div class="box" style="min-width: 30vh;" v-if="processingAPIRequest">
          <progress class="progress is-medium is-primary" max="100"></progress>
        </div>
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
    <section v-if="output && lastAPICalled == social_score">
      <div class="is-size-4 is-uppercase has-text-weight-bold has-text-centered has-text-white-ter">
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
      lastAPICalled: '',

      // endpoints
      job_title: 'https://jobtitle-mu7u3ykctq-lz.a.run.app/api/job_title',
      social_score: 'https://socialscore-mu7u3ykctq-lz.a.run.app/api/social_score',
      // 'https://socialscore-mu7u3ykctq-lz.a.run.app/api/social_score'
      // 'http://localhost:8080/api/social_score'

      // table data
      gridData: [
        {'person': 'Elon Musk', 'web_score': 1.0, 'google_items': 54300000, 'wiki_items': 857, 'twtr_users': 20, 'twtr_followers': 33221297, 'ig_users': 47, 'ig_followers': 739500},
        {'person': 'Albert Einstein', 'web_score': 1.0, 'google_items': 53100000, 'wiki_items': 4633, 'twtr_users': 20, 'twtr_followers': 149914, 'ig_users': 16, 'ig_followers': 826200},
        {'person': 'Nicki Minaj', 'web_score': 1.0, 'google_items': 79500000, 'wiki_items': 2816, 'twtr_users': 20, 'twtr_followers': 20519671, 'ig_users': 53, 'ig_followers': 108100},
        {'person': 'Charles Darwin', 'web_score': 0.98, 'google_items': 19000000, 'wiki_items': 3975, 'twtr_users': 20, 'twtr_followers': 2907030, 'ig_users': 17, 'ig_followers': 629},
        {'person': 'Bart Simpson', 'web_score': 0.97, 'google_items': 16000000, 'wiki_items': 427, 'twtr_users': 20, 'twtr_followers': 46493, 'ig_users': 26, 'ig_followers': 977},
        {'person': 'Karolina Meschino', 'web_score': 0.86, 'google_items': 435000, 'wiki_items': 4, 'twtr_users': 1, 'twtr_followers': 132, 'ig_users': 31, 'ig_followers': 298200}
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
      var url = endpoint + "?input=" + this.input
      axios.get(url).then(function (response){
          vm.output = response.data
          vm.processingAPIRequest = false
          vm.lastAPICalled = endpoint
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
          'web_score': this.output['scores']['web_score'],
          'google_items': this.output['data']['google']['items'],
          'wiki_items': this.output['data']['wikipedia']['items'],
          'twtr_users': this.output['data']['twitter']['num_users'],
          'twtr_followers': this.checkIfArrayIsEmpty(this.output['data']['twitter']['users'], 0)['followers_count'],
          'ig_users': this.output['data']['instagram']['num_users'],
          'ig_followers': this.checkIfArrayIsEmpty(this.output['data']['instagram']['users'], 0)['followers_count'],
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

.fade-enter-active, .fade-leave-active {
  transition: opacity 1s;
}

.fade-enter, .fade-leave-to /* .fade-leave-active below version 2.1.8 */ {
  opacity: 0;
}

.vjs-tree {
  font-size: 10px !important;
}

</style>
