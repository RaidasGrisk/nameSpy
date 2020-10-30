<template>
  <div>
    <div class="container">
      <div class="columns">

        <!-- Left col -->
        <div class="column is-two-third">
          <h1 class="title has-text-success">
            Enough explaining. <br>
            Try it out yourself!
          </h1>
          <h2 class="subtitle has-text-grey-darker">
            type in a name and see what's up
          </h2>
          <div class="field has-addons">
            <p class="control">
              <input class="input is-small" v-model='input' type="text" placeholder="e.g. Bart Simpson">
            </p>
          </div>
          <br>
          <div class="has-text-grey-darker">
            Or read the <router-link to="/Docs">Docs</router-link> 📖
          </div>
        </div>

        <!-- Right col -->
        <div class="column">
          <div class="box has-text-left has-background-white-ter">

            <div class="field has-addons">
              <p class="control">
                <a class="button is-primary is-focused is-small" @click="getModelApiData(url_webscore)">
                  web_score
                </a>
              </p>
              <p class="control is-expanded ">
                <input class="input is-small has-text-grey" v-bind:value="parseUrl(url_webscore, input)" readonly>
              </p>
            </div>

            <div class="field has-addons">
              <p class="control">
                <a class="button is-primary is-focused is-small" @click="getModelApiData(url_jobtitle)" style="padding-right:30px">
                  job_title
                </a>
              </p>
              <p class="control is-expanded ">
                <input class="input is-small has-text-grey" v-bind:value="parseUrl(url_jobtitle, input)" readonly>
              </p>
            </div>

            <div v-if="processingAPIRequest || output">
            <div class="box" style="max-height: 15rem; overflow: auto;">
              <div v-if="processingAPIRequest">
                <div class="loader"></div>
              </div>
              <div v-else>
                <div v-if="output">
                  <vue-json-pretty
                    :data="this.output"
                    :showLine="false"
                    :showDoubleQuotes="false">
                  </vue-json-pretty>
                </div>
              </div>
            </div>
          </div>
        </div>
        </div>
      </div>
    </div>

  </div>
</template>

<script>

import VueJsonPretty from 'vue-json-pretty'
import axios from 'axios'

export default {
  name: 'Service',
  components: {
    VueJsonPretty
  },

  data() {
    return {
      input: '',
      isActive: 'webscore',
      // end point params
      country_code: 'us',
      url_webscore: 'https://namespy-api-mu7u3ykctq-lz.a.run.app/v1/web_score',
      url_jobtitle: 'https://namespy-api-mu7u3ykctq-lz.a.run.app/v1/job_title',
      output: '',
      processingAPIRequest: false,
    }
  },

  methods: {
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

    parseUrl(url, param) {
      return url  + '?input=' + param
    }
  },

  mounted() {

    // Get the current location of the user:
    // Use it as input into the API call country
    var vm = this

    // http://ip-api.com/json/
    // wont work if the website use SSL

    // api.ipify.org + api.ipstack.com
    // not as nice as it needs to call multiple APIs

    // https://geolocation-db.com/json/
    axios.get('https://geolocation-db.com/json/').then(function (response){
        vm.country_code = response.data['country_code'].toLowerCase()
      }
    )
  }
}
</script>

<style>

.loader {
  border: 3px solid #FFFFFF; /* Light grey */
  border-top: 3px solid #8338EC; /* Blue */
  border-radius: 50%;
  width: 20px;
  height: 20px;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* vue-json-pretty font size: style tag must not be scoped */
.vjs-tree {
  font-size: 10px !important;
}

</style>
