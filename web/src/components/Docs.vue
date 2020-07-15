<template>
  <div>

<!-- https://www.npmjs.com/package/vue-scrollto -->

    <section class="main-content columns is-fullheight">

      <aside class="column is-3 is-narrow-mobile is-hidden-mobile is-fullheight section left-menu">
        <p class="menu-label">Documentation</p>
        <ul class="menu-list">
          <li>
            <a href="#intro" v-bind:class="{'is-active': activeMenuClass('intro')}" v-on:click="activeMenuItem = 'intro'" >
              <span class="icon"><i class="fa fa-home"></i></span>Intro
            </a>
          </li>
          <li>
            <a href="#endpoints" v-bind:class="{'is-active': activeMenuClass('endpoints')}" v-on:click="activeMenuItem = 'endpoints'">
              <span class="icon"><i class="fa fa-table"></i></span>Endpoints
            </a>
            <ul>
              <li>
                <a href="#webscore" v-bind:class="{'is-active': activeMenuClass('webscore')}" v-on:click="activeMenuItem = 'webscore'">
                  <span class="icon is-small"><i class="fa fa-link"></i></span>Web score
                </a>
              </li>
              <li>
                <a href="#occupation" v-bind:class="{'is-active': activeMenuClass('occupation')}" v-on:click="activeMenuItem = 'occupation'">
                  <span class="icon is-small"><i class="fa fa-link"></i></span>Occupation
                </a>
              </li>
            </ul>
          </li>
          <li>
            <a href="#about" v-bind:class="{'is-active': activeMenuClass('about')}" v-on:click="activeMenuItem = 'about'">
              <span class="icon"><i class="fa fa-info"></i></span>About
            </a>
          </li>
        </ul>
      </aside>

      <div class="container column is-6">
        <div class="section">

          <div id="intro" class="card">
            <div class="card-header"><p class="card-header-title">Intro</p></div>
            <div class="card-content">
              <div class="content">Endpoints:
              <ul><b>web-score</b> returns a score and the collected data (optional) asociated with how well a particular name is known on the internet and social networks.
              The web-score ranges between -1 and 1, where 0 is an average person, 1 is a super-star, -1 is someone totally unknown.</ul>
              <ul><b>occupation</b> returns a list of job and occupation titles as well as its sources (urls) related to the name.</ul>

              </div>
            </div>
          </div>
          <br />

          <div id="endpoints"></div>
          <div id="webscore"><docsBlockWebScore/></div><br/>
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

import docsBlockWebScore from './DocsBlockWebScore'
import docsBlockOccupation from './DocsBlockOccupation'

export default {

  name: 'docs',

  components: {
    docsBlockWebScore,
    docsBlockOccupation
  },

  data() {
    return {
      activeMenuItem: 'intro',
      idBlocks: ['intro', 'endpoints', 'webscore', 'occupation', 'about']
    }
  },

  methods: {

    activeMenuClass(item) {
      return item == this.activeMenuItem
    },

    // https://jschof.com/vue/scroll-tracking-in-vue-applications-some-gotchas/
    // utility copied from https://stackoverflow.com/questions/123999/how-to-tell-if-a-dom-element-is-visible-in-the-current-viewport
    elementInViewport(el) {
      var top = el.offsetTop;
      var height = el.offsetHeight;
      var bottom = top + height;

      while(el.offsetParent) {
        el = el.offsetParent;
        top += el.offsetTop;
      }

      return (
        !(top < window.pageYOffset && bottom < window.pageYOffset) &&
          !(top > (window.pageYOffset + (window.innerHeight)) && bottom > window.pageYOffset + (window.innerHeight))
      );
    },

    handleScroll() {
      const elementsInViewArray = this.idBlocks.map(number => {
        const el = document.getElementById(number);
        if(this.elementInViewport(el)) {
          return number;
        }
      });

      this.activeMenuItem = elementsInViewArray.find(number => number)
    }

  },

  created() {
    document.addEventListener('scroll', this.handleScroll);
  },
  destroyed() {
    document.removeEventListener('scroll', this.handleScroll);
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
