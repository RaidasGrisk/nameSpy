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
            NameSpy
          </div>
          <div class="content is-size-7 has-text-weight-bold has-text-success">
            I am a REST API service
          </div>
          <div class="content is-size-4">
            🧐
          </div>
        </div>
      </transition>

        <!-- <div class="content"> -->
        <transition name="fade" mode="out-in" appear>
          <div class="section" style="transition-delay: 1.2s">
            <div class="is-size-4 is-uppercase has-text-weight-bold">
              <p>What I do?</p>
            </div>
            <div class="is-size-7"  style="transition-delay: 0.9s">
              <p>
                You give me a name <br>
                I give you what I know about it:
              </p>
            </div>
            <div class="is-size-7 has-text-weight-bold has-text-success">
              <p>
                web score<br>
                occupation
              </p>
            </div>

          </div>
        </transition>


        <transition name="fade" mode="out-in" appear>
          <div class="section" style="transition-delay: 1.8s">
            <div class="is-size-4 is-uppercase has-text-weight-bold">
              <p>Enough talk, <br>try me</p>
            </div>

            <div class="content is-size-7">
              <p>Read the
                <router-link to="/Docs" class="has-text-success">DOCS</router-link>
                or <br>type in a name and see what's up</p>
            </div>

            <div class="field has-addons has-addons-centered">
              <p class="control">
                <input class="input is-small" v-model='input' type="text" placeholder="e.g. Bart Simpson">
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
        <div class="box has-text-centered" style="min-width: 30vh;" v-if="processingAPIRequest">
          <progress class="progress is-small is-primary" max="100"></progress>
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
      job_title: 'https://namespy-api-mu7u3ykctq-lz.a.run.app/v1/job_title',
      social_score: 'https://namespy-api-mu7u3ykctq-lz.a.run.app/v1/web_score',

      // end point params
      country_code: 'us',

      // table data
      gridData: [
        {'person': 'Albert Einstein', 'web_score': 1.0, 'google_items': 59100000, 'wiki_items': 4769, 'twtr_users': 20, 'twtr_followers': 1699679, 'ig_users': 21, 'ig_followers': 828300},
        {'person': 'Nicki Minaj', 'web_score': 1.0, 'google_items': 84600000, 'wiki_items': 2842, 'twtr_users': 20, 'twtr_followers': 20533394, 'ig_users': 49, 'ig_followers': 114572876},
        {'person': 'Elon Musk', 'web_score': 1.0, 'google_items': 70000000, 'wiki_items': 873, 'twtr_users': 20, 'twtr_followers': 34195789, 'ig_users': 47, 'ig_followers': 852900},
        {'person': 'Charles Darwin', 'web_score': 0.79, 'google_items': 20100000, 'wiki_items': 3997, 'twtr_users': 20, 'twtr_followers': 2913852, 'ig_users': 21, 'ig_followers': 657},
        {'person': 'Bart Simpson', 'web_score': 0.98, 'google_items': 15700000, 'wiki_items': 426, 'twtr_users': 20, 'twtr_followers': 47348, 'ig_users': 37, 'ig_followers': 97200},
        {'person': 'Karolina Meschino', 'web_score': 0.86, 'google_items': 614000, 'wiki_items': 4, 'twtr_users': 1, 'twtr_followers': 134, 'ig_users': 30, 'ig_followers': 303700}
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

      axios.get(endpoint, {
        params: {
          'input': vm.input,
          'country_code': vm.country_code,
          'filter_input': 1,
          'use_proxy': 1,
          'collected_data': 1
        }
      }).then(function (response){
          vm.output = response.data
          vm.processingAPIRequest = false
          vm.lastAPICalled = endpoint
      }).catch(function (error){
        vm.output = error.response.data
        vm.processingAPIRequest = false
      })
    },

    // Retruns the max of followers for the grid data
    getFollowersNumber(array) {
      var followers = []
      array.forEach(function (arrayItem) {
        followers.push(arrayItem.followers_count)
      })

      if (followers.length > 0) {
        return Math.max(...followers)
      } else {
        return 0
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
          'twtr_followers': this.getFollowersNumber(this.output['data']['twitter']['users']),
          'ig_users': this.output['data']['instagram']['num_users'],
          'ig_followers': this.getFollowersNumber(this.output['data']['instagram']['users']),
          'class': 'is-success'
        }
        this.gridData.push(newRow)
      }
      return this.gridData
    }
  },

  mounted() {

    // Get the current location of the user:
    // Use it as input into the API call country
    var vm = this

    // http://ip-api.com/json/
    // wont work if the website use SSL
    // axios.get('http://ip-api.com/json/').then(function (response){
    //     vm.country_code = response.data['countryCode'].toLowerCase()
    //   }
    // )

    // https://geolocation-db.com/json/
    axios.get('https://geolocation-db.com/json/').then(function (response){
        vm.country_code = response.data['country_code'].toLowerCase()
      }
    )

    // api.ipify.org + api.ipstack.com
    // not as nice as it neets to call multiple APIs
    // axios.get('https://api.ipify.org/?format=json').then(function (response){
    //
    //   // get the location of the client and set API param
    //   let access_key = 'fb7f9964a23b45a6a28debbc8115226f'
    //   let ip_address = response.data['ip']
    //   axios.get(`http://api.ipstack.com/${ip_address}?access_key=${access_key}`).then(function (response){
    //       vm.country_code = response.data['country_code'].toLowerCase()
    //   })
    // })
  }
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
