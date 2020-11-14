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
            Or read the <router-link class="has-text-danger" to="/Docs">Docs</router-link> 📖
          </div>
        </div>

        <!-- Right col -->
        <div class="column">
          <div class="box has-text-left has-background-white-ter">

            <div class="field has-addons">
              <p class="control">
                <a class="button is-primary is-focused is-small" @click="getModelApiData(url_webscore, webscore_params)">
                  web_score
                </a>
              </p>
              <p class="control is-expanded">
                <input class="input is-small has-text-grey"
                v-bind:value="removeUrlBase(parseUrl(url_webscore, webscore_params))" readonly>
              </p>
              <a class="button is-small has-text-primary" @click="copyRefText('web_score_url')">
                <font-awesome-icon :icon="['fa', 'copy']"/>
              </a>
            </div>

            <div class="field has-addons">
              <p class="control">
                <a class="button is-primary is-focused is-small" @click="getModelApiData(url_jobtitle, jobtitle_params)" style="padding-right:30px">
                  job_title
                </a>
              </p>
              <p class="control is-expanded">
                <input class="input is-small has-text-grey"
                v-bind:value="removeUrlBase(parseUrl(url_jobtitle, jobtitle_params))" readonly>
              </p>
              <a class="button is-small has-text-primary" @click="copyRefText('job_title_url')">
                <font-awesome-icon :icon="['fa', 'copy']"/>
              </a>
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

    <!-- Hidden text are to copy from -->
    <!-- style="visibility: hidden" -->
    <!-- https://stackoverflow.com/questions/49053240/hidden-element-wont-copy-to-clipboard -->
    <div style="position: absolute; left: -999em;" aria-hidden="true">
      <textarea ref="web_score_url" v-bind:value="parseUrl(url_webscore, webscore_params)"></textarea>
      <textarea ref="job_title_url" v-bind:value="parseUrl(url_jobtitle, jobtitle_params)"></textarea>
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

      // api input/output
      input: '',
      output: '',

      // end point params
      url_webscore: 'https://namespy-api-mu7u3ykctq-lz.a.run.app/v1/web_score',
      url_jobtitle: 'https://namespy-api-mu7u3ykctq-lz.a.run.app/v1/job_title',
      webscore_params: {
        // 'input': '',
        // 'country_code': '',
        'filter_input': 1,
        'use_proxy': 1,
        'debug': 0,
        'collected_data': 1,
      },
      jobtitle_params: {
        // 'input': '',
        // 'country_code': '',
        'filter_input': 1,
        'use_proxy': 1,
        'debug': 0
      },

      // other
      processingAPIRequest: false,
    }
  },

  methods: {
    getModelApiData(endpoint, params) {

      this.output = null
      this.processingAPIRequest = true
      var vm = this
      var parsed_params = {...{'input': vm.input}, ...params}

      axios.get(endpoint, {params: parsed_params}
      ).then(function (response){
        vm.output = response.data
        vm.processingAPIRequest = false
      }).catch(function (error){
        vm.output = error.response.data
        vm.processingAPIRequest = false
      })
    },

    parseUrl(url, params) {
      var parsed_params = {...{'input': this.input}, ...params}
      var parsed_url = url + '?'
      for (var key in parsed_params) {
        parsed_url += key + '=' + parsed_params[key] + '&'
      }
      return parsed_url.slice(0, -1)
    },

    removeUrlBase(url) {
      // https://stackoverflow.com/questions/14480345/how-to-get-the-nth-occurrence-in-a-string
      var base_ending_index = url.split('/', 3).join('/').length;
      return url.slice(base_ending_index)
    },

    copyRefText(ref) {
      this.$refs[ref].select();
      document.execCommand('copy');
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
        vm.webscore_params['country_code'] = response.data['country_code'].toLowerCase()
        vm.jobtitle_params['country_code'] = response.data['country_code'].toLowerCase()
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
