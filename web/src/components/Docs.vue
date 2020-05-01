<template>
  <div>

<!-- https://www.npmjs.com/package/vue-scrollto -->

    <section class="main-content columns is-fullheight">

      <aside class="column is-2 is-narrow-mobile is-hidden-mobile is-fullheight section left-menu">
        <p class="menu-label">Documentation</p>
        <ul class="menu-list">
          <li>
            <a href="#" v-bind:class="{'is-active': activeMenuItem == 'Home'}" v-on:click="activeMenuItem = 'Home'">
              <span class="icon"><i class="fa fa-home"></i></span> Home
            </a>
          </li>
          <li>
            <a href="#Endpoints" v-bind:class="{'is-active': activeMenuItem == 'Endpoints'}" v-on:click="activeMenuItem = 'Endpoints'">
              <span class="icon"><i class="fa fa-table"></i></span> Endpoints
            </a>
            <ul>
              <li>
                <a href="#Endpoints" v-bind:class="{'is-active': activeMenuItem == 'web score'}" v-on:click="activeMenuItem = 'web score'">
                  <span class="icon is-small"><i class="fa fa-link"></i></span> web score
                </a>
              </li>
              <li>
                <a href="#occupation" v-bind:class="{'is-active': activeMenuItem == 'occupation'}" v-on:click="activeMenuItem = 'occupation'">
                  <span class="icon is-small"><i class="fa fa-link"></i></span> occupation
                </a>
              </li>
            </ul>
          </li>
          <li>
            <a href="#data and about" v-bind:class="{'is-active': activeMenuItem == 'Data and about'}" v-on:click="activeMenuItem = 'Data and about'">
              <span class="icon"><i class="fa fa-info"></i></span> Data and about
            </a>
          </li>
        </ul>
      </aside>

      <div class="container column is-7">
        <div class="section">

          <div class="card">
            <div class="card-header"><p class="card-header-title">Home</p></div>
            <div class="card-content"><div class="content">List of endpoints:
              <ul><b>web-score</b> returns a score and the data collected (optional) asociated with how well a particular name is known on the internet and social networks.
              The web-score ranges between -1 and 1, where 0 is an average person, 1 is a super-star, -1 is someone totally unknown.</ul>
              <ul><b>occupation</b> returns a list of job and occupation titles as well as its sources (url links) related to particular person.</ul>

            </div></div>
          </div>
          <br />

          <div class="card is-hidden1" id="Endpoints">
            <div class="card-header"><p class="card-header-title">Endpoint: web score</p></div>
            <div class="card-content">
              <div class="content">

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
          <br />

          <div class="card is-hidden1" id="occupation">
            <div class="card-header"><p class="card-header-title">Endpoint: occupation</p></div>
            <div class="card-content">
              <div class="content">

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
                    <pre>{{python_code}}</pre>
                  </div>
                  <div class="content" v-bind:class="{'is-active': isActive == 'Bash'}">
                    <pre>{{bash_code}}</pre>
                  </div>
                  <div class="content" v-bind:class="{'is-active': isActive == 'Javascript'}">
                    <pre>{{javascript_code}}</pre>
                  </div>
                  <div class="content" v-bind:class="{'is-active': isActive == 'Golang'}">
                    <pre>{{golang_code}}</pre>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <br />

          <div class="card is-hidden1" id="data and about">
            <div class="card-header"><p class="card-header-title">Data and About</p></div>
            <div class="card-content">
              <div class="content">

              </div>
            </div>
          </div>
          <br />

        </div>
      </div>

    </section>

  </div>
</template>

<script>

export default {

  name: 'docs',

  components: {
  },

  data() {
    return {
      activeMenuItem: 'Home',
      isActive: 'Python',

      python_code: `
import requests

url = 'https://socialscore-mu7u3ykctq-lz.a.run.app/api/social_score?'

payload = {
    'input': 'Bart Simpson',
    'filter_input': 0,
    'use_proxy': 1,
    'return_data': 1
}

response = requests.get(url, params=payload)
print(response.json())
      `,

      bash_code: `
curl -G "https://socialscore-mu7u3ykctq-lz.a.run.app/api/social_score" \
  --data-urlencode "input=bart simpson" \
  --data-urlencode "filter_input=0" \
  --data-urlencode "use_proxy=1" \
  --data-urlencode "return_data=1"
      `,

      javascript_code: `
const options = {
  url: 'https://socialscore-mu7u3ykctq-lz.a.run.app/api/social_score',
  method: 'GET',
  data: {
    input: "bart simpson",
    filter_input: 1,
    use_proxy: 1,
    return_data: 1,
  }
};

axios(options)
  .then(response => {
    console.log(response.status);
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

.main-content {
  padding-bottom: 2rem;
  background-color: #F0F0F0;
}

.left-menu {
  padding-bottom: 2rem;
  background-color: #F0F0F0;
  position: fixed;
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
