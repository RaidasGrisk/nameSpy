<template>
  <div class="card is-hidden1">
    <div class="card-header"><p class="card-header-title">Endpoint: occupation</p></div>
    <div class="card-content">
      <div class="content">

        <p><pre class='code'>https://jobtitle-mu7u3ykctq-lz.a.run.app/api/job_title</pre></p>

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
            <tr v-for="value in argsTable" :key="value">
              <td>{{ value[0] }}</td>
              <td>{{ value[1] }}</td>
              <td><span v-html="value[2]"></span></td>
            </tr>
          </tbody>
        </table>

        <div class="tabs">
          <ul>
            <li v-bind:class="{'is-active': isActive == 'Python'}"><a v-on:click="isActive = 'Python'">Python</a></li>
            <li v-bind:class="{'is-active': isActive == 'Bash'}"><a v-on:click="isActive = 'Bash'">Bash</a></li>
            <li v-bind:class="{'is-active': isActive == 'Javascript'}"><a v-on:click="isActive = 'Javascript'">Javascript</a></li>
            <li v-bind:class="{'is-active': isActive == 'Golang'}"><a v-on:click="isActive = 'Golang'">Golang</a></li>
          </ul>
        </div>

        <div class="tab-contents">
          <div class="content" v-bind:class="{'is-active': isActive == 'Python'}">
            <pre class='code'>{{python_code}}</pre>
          </div>
          <div class="content" v-bind:class="{'is-active': isActive == 'Bash'}">
            <pre class='code'>{{bash_code}}</pre>
          </div>
          <div class="content" v-bind:class="{'is-active': isActive == 'Javascript'}">
            <pre class='code'>{{javascript_code}}</pre>
          </div>
          <div class="content" v-bind:class="{'is-active': isActive == 'Golang'}">
            <pre class='code'>{{golang_code}}</pre>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>

export default {

  name: 'docsOccupation',

  components: {
  },

  data() {
    return {

      argsTable: [
        ['input', 'string', 'first name last name'],
        ['filter_input (optional)', 'int', '1 to filter input by detecting name and surname, 0 not to. Default value 1'],
        ['use_proxy (optional)', 'int', '1 to use proxy while collecting data, 0 not to. Implemented due to bypass google/IG scrape detection. Default value 0'],
        ['ner_threshold (optional)', 'float', 'Detection probability threshold of word asociated with occupation/job-titles. Lower threshold implies looser detection. Default value 0.95 (returns words that are detected as occupation/job-title with probability of >95%)'],
        ['country_code (optional)', 'string', 'Country code through which to do the google search. Provide the value if known, this improves the results. <a href="https://developers.google.com/custom-search/docs/xml_results_appendices#countryCodes" target="_blank">Available country codes</a>. Default value us']
      ],

      isActive: 'Python',

      python_code: `
import requests

url = 'https://jobtitle-mu7u3ykctq-lz.a.run.app/api/job_title'

payload = {
    'input': 'Bart Simpson',
    'filter_input': 0,
    'use_proxy': 1,
    'ner_threshold': 0.95,
    'country_code': 'us',
}

response = requests.get(url, params=payload)
print(response.json())
      `,

      bash_code: `
curl -G "https://jobtitle-mu7u3ykctq-lz.a.run.app/api/job_title" \\
  --data-urlencode "input=bart simpson" \\
  --data-urlencode "filter_input=0" \\
  --data-urlencode "use_proxy=1" \\
  --data-urlencode "ner_threshold=0.95" \\
  --data-urlencode "country_code=us"
      `,

      javascript_code: `
const options = {
  url: 'https://jobtitle-mu7u3ykctq-lz.a.run.app/api/job_title',
  method: 'GET',
  data: {
    input: "bart simpson",
    filter_input: 1,
    use_proxy: 1,
    ner_threshold: 0.95,
    country_code: "us"
  }
};

axios(options)
  .then(response => {
    console.log(response.data);
  });
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

.code {
  font-size: 11px;
}

/* This is related to bulma tabs
It hides, shows the content */
.tab-contents .content {
  display: none;
}
.tab-contents .content.is-active {
  display: block;
}

</style>
