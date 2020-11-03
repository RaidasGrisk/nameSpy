<template>

  <!-- https://www.npmjs.com/package/vue-scrollto -->
  <section class="main-content columns is-fullheight">

    <aside class="column is-2 is-narrow-mobile is-hidden-mobile is-fullheight section left-menu">
      <p class="menu-label">Documentation</p>
      <ul class="menu-list">

        <li>
          <a href="#endpoints" v-bind:class="{'is-active': activeMenuClass('endpoints')}" v-on:click="activeMenuItem = 'endpoints'">
            Endpoints
          </a>
          <ul>
            <li>
              <a href="#webscore" v-bind:class="{'is-active': activeMenuClass('webscore')}" v-on:click="activeMenuItem = 'webscore'">
                Web score
              </a>
            </li>
            <li>
              <a href="#occupation" v-bind:class="{'is-active': activeMenuClass('occupation')}" v-on:click="activeMenuItem = 'occupation'">
                Occupation
              </a>
            </li>
          </ul>
        </li>
        <li>
          <a href="#about" v-bind:class="{'is-active': activeMenuClass('about')}" v-on:click="activeMenuItem = 'about'">
            About
          </a>
        </li>
      </ul>
    </aside>

    <div class="container column is-6">
      <div class="section">
        <div id="endpoints"></div>
        <div id="webscore"><docsBlockWebScore/></div><br/>
        <div id="occupation"><docsBlockOccupation/></div><br/>
        <div id="about"><aboutBlock/></div><br/>
      </div>
    </div>

  </section>

</template>

<script>

import docsBlockWebScore from '@/components/docs/DocsBlockWebScore'
import docsBlockOccupation from '@/components/docs/DocsBlockOccupation'
import aboutBlock from '@/components/docs/AboutBlock'


export default {

  name: 'docs',

  components: {
    docsBlockWebScore,
    docsBlockOccupation,
    aboutBlock
  },

  data() {
    return {
      activeMenuItem: 'endpoints',
      idBlocks: ['endpoints', 'webscore', 'occupation', 'about']
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
