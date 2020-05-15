<template>
  <div class="card is-hidden1">
    <div class="card-header"><p class="card-header-title">Endpoint: web score</p></div>
    <div class="card-content">
      <div class="content">

        <p><pre class='code' style="font-size: 11px">https://socialscore-mu7u3ykctq-lz.a.run.app/api/social_score</pre></p>

        <table class="table is-narrow is-fullwidth is-hoverable" style="font-size: 11px !important;">
          <thead>
            <th v-for="key in ['Parameter', 'type', '']" :key="key">
              {{ key }}
            </th>
          </thead>
          <tfoot>
          </tfoot>
          <tbody>
            <!-- iter over entry and idx, to dodge vue warn of using non-primitive value as key -->
            <tr v-for="(value, idx) in argsTable" :key="idx">
              <td>{{ value[0] }}</td>
              <td>{{ value[1] }}</td>
              <td>{{ value[2] }}</td>
            </tr>
          </tbody>
        </table>

        <div class="tabs is-small">
          <ul>
            <li v-bind:class="{'is-active': isActive == 'Python'}">
              <a v-on:click="isActive = 'Python'">
                <span class="icon is-small"><font-awesome-icon :icon="['fab', 'python']" /></span>
                <span>py</span>
              </a>
            </li>

            <li v-bind:class="{'is-active': isActive == 'Bash'}">
              <a v-on:click="isActive = 'Bash'">
                <span class="icon is-small"><font-awesome-icon :icon="['fa', 'terminal']" /></span>
                <span>bash</span>
              </a>
            </li>

            <li v-bind:class="{'is-active': isActive == 'Javascript'}">
              <a v-on:click="isActive = 'Javascript'">
                <span class="icon is-small"><font-awesome-icon :icon="['fab', 'js']" /></span>
                <span>js</span>
              </a>
            </li>

            <li v-bind:class="{'is-active': isActive == 'Golang'}">
              <a v-on:click="isActive = 'Golang'">
                <span class="icon is-small"><img src="https://img.icons8.com/ios/50/000000/golang.png"/></span>
                <span>go</span>
              </a>
            </li>
          </ul>
        </div>

        <div class="tab-contents">
          <div class="content" v-bind:class="{'is-active': isActive == 'Python'}">
            <prism-editor :code="python_code" language="python"/>
          </div>
          <div class="content" v-bind:class="{'is-active': isActive == 'Bash'}">
            <prism-editor :code="bash_code" language="js"/>
          </div>
          <div class="content" v-bind:class="{'is-active': isActive == 'Javascript'}">
            <prism-editor :code="javascript_code" language="js"/>
          </div>
          <div class="content" v-bind:class="{'is-active': isActive == 'Golang'}">
            <prism-editor :code="golang_code" language="js"/>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>

// import prismjs and color scheme for code highlight
import "prismjs"
import './prism-ghcolors.css'
import "prismjs/components/prism-python.js"
import PrismEditor from 'vue-prism-editor'

export default {

  name: 'docsWebScore',

  components: {
    PrismEditor
  },

  data() {
    return {

      argsTable: [
        ['input', 'string', 'first name last name'],
        ['filter_input (optional)', 'int', '1 to filter input by detecting name and surname, 0 not to. Default value 1'],
        ['use_proxy (optional)', 'int', '1 to use proxy while collecting data, 0 not to. Implemented to bypass google/IG scrape detection. Default value 0'],
        ['collected_data (optional)', 'int', 'return detailed data that is collected during the scoring process. Default value 1']
      ],

      isActive: 'Python',


      // code examples for each lang
      python_code: `
import requests

url = 'https://socialscore-mu7u3ykctq-lz.a.run.app/api/social_score'

payload = {
    'input': 'Bart Simpson',
    'filter_input': 0,
    'use_proxy': 1,
    'collected_data': 1
}

response = requests.get(url, params=payload)
print(response.json())
      `,

      bash_code: `
curl -G "https://socialscore-mu7u3ykctq-lz.a.run.app/api/social_score" \\
  --data-urlencode "input=bart simpson" \\
  --data-urlencode "filter_input=0" \\
  --data-urlencode "use_proxy=1" \\
  --data-urlencode "collected_data=1"
      `,

      javascript_code: `
import axios from "axios"

const options = {
  url: 'https://socialscore-mu7u3ykctq-lz.a.run.app/api/social_score',
  method: 'GET',
  data: {
    input: "bart simpson",
    filter_input: 1,
    use_proxy: 1,
    collected_data: 1,
  }
};

axios(options)
  .then(response => {
    console.log(response.data);
  });
      `,

      golang_code: `
package main

import (
    "fmt"
    "io/ioutil"
    "log"
    "net/http"
    "os"
    "net/url"
)

func main() {

    baseUrl, err := url.Parse("https://socialscore-mu7u3ykctq-lz.a.run.app/api/social_score")

    params := url.Values{}
    params.Add("input", "Bart Simpson")
    params.Add("filter_input", "1")
    params.Add("use_proxy", "1")
    params.Add("collected_data", "1")
    baseUrl.RawQuery = params.Encode()

    response, err := http.Get(baseUrl.String())

    if err != nil {
        fmt.Print(err.Error())
        os.Exit(1)
    }

    responseData, err := ioutil.ReadAll(response.Body)
    if err != nil {
        log.Fatal(err)
    }
    fmt.Println(string(responseData))

}
      `


    }
  },

  methods: {

    },
  computed: {

  },

}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style>

/* This is related to bulma tabs
It hides, shows the content */
.tab-contents .content {
  display: none;
}
.tab-contents .content.is-active {
  display: block;
}

/* This is for prism not to conflict with bulma */
/* https://github.com/jgthms/bulma/issues/1708 */
.content .tag, .content .number {
  display: inline;
  padding: inherit;
  font-size: inherit;
  line-height: inherit;
  text-align: inherit;
  vertical-align: inherit;
  border-radius: inherit;
  font-weight: inherit;
  white-space: inherit;
  background: inherit;
  margin: inherit;
}

/* this is to fix editor box */
/* div.prism-editor-wrapper {
    max-height: 250px;
    min-height: 250px;
    overflow-y: auto;
} */

</style>
