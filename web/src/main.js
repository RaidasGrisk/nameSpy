import Vue from 'vue'
import App from './App.vue'
import router from './router'

// Fontawsome
import { library } from '@fortawesome/fontawesome-svg-core'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
Vue.component('font-awesome-icon', FontAwesomeIcon)

import { faPython, faJs, faLinux } from '@fortawesome/free-brands-svg-icons'
import { faTerminal } from '@fortawesome/free-solid-svg-icons'
library.add(faPython, faJs, faLinux, faTerminal)

Vue.config.productionTip = false

new Vue({
  router,
  render: h => h(App),
}).$mount('#app')
