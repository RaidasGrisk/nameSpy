<template>
  <div class="card is-hidden1">
    <div class="card-header"><p class="card-header-title">{{ title }}</p></div>
    <div class="card-content">
      <div class="content">

        <p><pre class='code' style="font-size: 11px">{{ endpoint_url }}</pre></p>

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
              <!-- this is to render url links properly -->
              <td><span v-html="value[2]"></span></td>
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
                <span>Curl</span>
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
            <prism-editor :code="py_example" language="python"/>
          </div>
          <div class="content" v-bind:class="{'is-active': isActive == 'Bash'}">
            <prism-editor :code="bash_example" language="js"/>
          </div>
          <div class="content" v-bind:class="{'is-active': isActive == 'Javascript'}">
            <prism-editor :code="js_example" language="js"/>
          </div>
          <div class="content" v-bind:class="{'is-active': isActive == 'Golang'}">
            <prism-editor :code="go_example" language="js"/>
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

  name: 'docsBlock',

  props: {
    title: String,
    endpoint_url: String,
    argsTable: Array,
    isActive: String,

    py_example: String,
    bash_example: String,
    js_example: String,
    go_example: String
  },

  components: {
    PrismEditor
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
