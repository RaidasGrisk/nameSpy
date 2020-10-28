<template>
  <body>
    <section class="hero is-medium">
      <div class="hero-head">
        <NavBar/>
      </div>

      <div class="hero-body">
        <div class="container">
          <div class="columns">

            <!-- The text on the left -->
            <div class="column is-one-third">
              <transition name="fade" mode="out-in" appear>
                <div style="transition-delay: 0.3s">
                  <h1 class="title">
                    Hi, my name is NAMESPY 🧐
                  </h1>
                  <h2 class="subtitle has-text-grey-darker">
                    I spy on names, duh.
                  </h2>
                  <br>
                  <h2 class="subtitle has-text-grey-darker">
                    I'll tell you who's famous🔥 and who's not
                    <!-- and if you'll dig deeper, you might find even more details -->
                    and if if you wish, will
                    the job title / occupation {{ this.currentEmoji }} behind the name
                  </h2>
                  <br>
                  <div class="has-text-grey-darker">
                    Use my <router-link to="/Docs">REST API</router-link> service
                    to get to know the names you've got!
                  </div>
                </div>
              </transition>
            </div>

            <div class="column is-one-third">
              <!-- Empty for the sake of allignment -->
            </div>

            <!-- the image on the right -->
            <div class="column is-one-third">
              <transition name="fade" mode="out-in" appear>
                <div style="transition-delay: 2s">
                  <div v-tilt="tiltOptions">
                    <div class="box has-text-centered has-background-primary">
                      <img src="@/assets/black.png" alt="Logo" style="width:200px; opacity: 0.4;">
                    </div>
                    <div class="has-text-grey-darker">
                      API status: <label v-html="statusEmoji"></label> <br>
                      Requests today: 10<br>
                      Requests total: 999
                    </div>
                  </div>
                </div>
              </transition>
            </div>

          </div>
        </div>
      </div>




    </section>
  </body>
</template>

<script>

import NavBar from '@/components/NavBar'
import axios from 'axios'

export default {
  name: 'Hero',
  components: {
    NavBar
  },

  data() {
    return {
      tiltOptions: {
        speed: 5000,
        perspective: 1000,
        glare: true,
        scale: 1,
        max: 20
      },

      currentEmoji: this.getJobEmoji(),

      system_status: undefined,
    }
  },

  methods: {
    getJobEmoji() {
      var emojis = ['🤺', '🚴', '🚀', '🤸', '🤹', '🎮', '🎨', '🎻', '🛰']
      return emojis[Math.floor(Math.random() * emojis.length)]
    },

    // draw random emoji every x secconds
    // executed inside creted (starts when created)
    setJobEmoji() {
      setInterval(() => {
        this.currentEmoji = this.getJobEmoji()
      }, 5000)
    }

  },

  computed: {
    statusEmoji() {
      // chec if undefined
      if (!this.system_status){
        console.log('asdasdasd')
        return '<label class="loader"></label>'
      }
      else {
        var firstChar = String(this.system_status).charAt(0)
        console.log(this.system_status)
        if (firstChar == '5'){
          return '🔴'
        } else {
          return '🟢'
        }

      }

    }
  },

  created() {
    this.setJobEmoji()
  },

  mounted() {

    var vm = this
    axios.get('https://namespy-api-mu7u3ykctq-lz.a.run.app/v1/web_score')
    .then(function (response){
      vm.system_status = response.status
      console.log(response.status)
    }).catch(function (error){
      vm.system_status = error.response.status
      console.log(error.response.status)
    })

  }

}
</script>

<style scoped>

/* https://codepen.io/P1N2O/pen/pyBNzX */
body {
  /* #ee7752, #e73c7e, #23a6d5, #23d5ab */
  /* https://coolors.co/ffbe0b-fb5607-ff006e-8338ec-3a86ff */
	background: linear-gradient(5deg, #8338EC, #8338EC, #8338EC, #FF006E, #FF006E);
	background-size: 400% 400%;
	animation: gradient 10s ease infinite;
}
@keyframes gradient {
	0% {
		background-position: 0% 50%;
	}
	50% {
		background-position: 100% 50%;
	}
	100% {
		background-position: 0% 50%;
	}
}

/* Spinnig Icon */
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

</style>
