import Vue from 'vue'
import App from './App.vue'
import router from './router'

// Fontawsome
import { library } from '@fortawesome/fontawesome-svg-core'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
Vue.component('font-awesome-icon', FontAwesomeIcon)

// Docs icons
import { faPython, faJs, faLinux } from '@fortawesome/free-brands-svg-icons'
import { faTerminal } from '@fortawesome/free-solid-svg-icons'
library.add(faPython, faJs, faLinux, faTerminal)

// Social icons
import { faTwitter, faGithub } from '@fortawesome/free-brands-svg-icons'
library.add(faTwitter, faGithub)

// Other icons
import { faCopy } from '@fortawesome/free-solid-svg-icons'
library.add(faCopy)

// tilt
import VueTilt from 'vue-tilt.js'
Vue.use(VueTilt)

Vue.config.productionTip = false

new Vue({
  router,
  render: h => h(App),
}).$mount('#app')
