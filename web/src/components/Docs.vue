<template>
  <div>

<!-- https://www.npmjs.com/package/vue-scrollto -->

    <section class="main-content columns is-fullheight">

      <aside class="column is-2 is-narrow-mobile is-hidden-mobile is-fullheight section left-menu">
        <p class="menu-label">Documentation</p>
        <ul class="menu-list">
          <li>
            <a href="#" v-bind:class="{'is-active': activeMenuItem == 'Home'}" v-on:click="activeMenuItem = 'Home'">
              <span class="icon"><i class="fa fa-home"></i></span>Intro
            </a>
          </li>
          <li>
            <a href="#endpoints" v-bind:class="{'is-active': activeMenuItem == 'Endpoints'}" v-on:click="activeMenuItem = 'Endpoints'">
              <span class="icon"><i class="fa fa-table"></i></span>Endpoints
            </a>
            <ul>
              <li>
                <a href="#endpoints" v-bind:class="{'is-active': activeMenuItem == 'web score'}" v-on:click="activeMenuItem = 'web score'">
                  <span class="icon is-small"><i class="fa fa-link"></i></span>Web score
                </a>
              </li>
              <li>
                <a href="#occupation" v-bind:class="{'is-active': activeMenuItem == 'occupation'}" v-on:click="activeMenuItem = 'occupation'">
                  <span class="icon is-small"><i class="fa fa-link"></i></span>Occupation
                </a>
              </li>
            </ul>
          </li>
          <li>
            <a href="#about" v-bind:class="{'is-active': activeMenuItem == 'Data and about'}" v-on:click="activeMenuItem = 'Data and about'">
              <span class="icon"><i class="fa fa-info"></i></span>About
            </a>
          </li>
        </ul>
      </aside>

      <div class="container column is-6">
        <div class="section">

          <div class="card">
            <div class="card-header"><p class="card-header-title">Intro</p></div>
            <div class="card-content">
              <div class="content">Endpoints:
              <ul><b>web-score</b> returns a score and the collected data (optional) asociated with how well a particular name is known on the internet and social networks.
              The web-score ranges between -1 and 1, where 0 is an average person, 1 is a super-star, -1 is someone totally unknown.</ul>
              <ul><b>occupation</b> returns a list of job and occupation titles as well as its sources (url links) related to the name.</ul>

              </div>
            </div>
          </div>
          <br />

          <div id="endpoints"><docsBlockWebScore/></div><br/>
          <div id="occupation"><docsBlockOccupation/></div><br/>

          <div class="card is-hidden1" id="about">
            <div class="card-header"><p class="card-header-title">About</p></div>
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

import docsBlockWebScore from './docsBlockWebScore'
import docsBlockOccupation from './docsBlockOccupation'

export default {

  name: 'docs',

  components: {
    docsBlockWebScore,
    docsBlockOccupation
  },

  data() {
    return {
      activeMenuItem: 'Home',
      isActive: 'Python'

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
