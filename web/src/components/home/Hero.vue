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
                  <h1 class="title has-text-success">
                    Hi, my name is NAMESPY 🧐
                  </h1>
                  <h2 class="subtitle has-text-black-ter">
                    I spy on names, duh.
                  </h2>
                  <br>
                  <h2 class="subtitle has-text-black-ter">
                    I'll tell you who's famous🔥 and who's not
                    <!-- and if you'll dig deeper, you might find even more details -->
                    and if you wish, will find
                    the job title / occupation {{ this.currentEmoji }} behind the name
                  </h2>
                  <br>
                  <div class="has-text-black-ter">
                    Use my <router-link class="has-text-danger" to="/Docs">REST API</router-link> service
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
                <div style="transition-delay: 0.3s">
                  <div v-tilt="tiltOptions">
                    <StatusBoard/>
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
import StatusBoard from '@/components/home/StatusBoard'

export default {
  name: 'Hero',
  components: {
    NavBar,
    StatusBoard
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

    }
  },

  methods: {
    getJobEmoji() {
      var emojis = ['🤺', '🚴', '🚀', '🤸', '🤹', '🎮', '🎨', '🎻', '🛰', '🦙', '🐿️', '👩‍💼', '🧠', '👾']
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

  },

  created() {
    this.setJobEmoji()
  },

  mounted() {

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

.fade-enter-active, .fade-leave-active {
  transition: opacity 1s;
}
.fade-enter, .fade-leave-to /* .fade-leave-active below version 2.1.8 */ {
  opacity: 0;
}

</style>
