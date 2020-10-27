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
            <div class="column is-three-quarters">
              <transition name="fade" mode="out-in" appear>
                <div style="transition-delay: 0.3s">
                  <h1 class="title">
                    Hi, my name is NAMESPY 🧐
                  </h1>
                  <h2 class="subtitle has-text-grey-darker">
                    I'll tell you who is famous🔥 and who's not <br>
                    and if you'll dig deeper, you might find even more details
                  </h2>
                  <br>
                  <div class="has-text-grey-darker">
                    Use my <router-link to="/Docs">REST API</router-link> service <br>
                    to get to know the names you've got
                  </div>
                </div>
              </transition>
            </div>

            <!-- the image on the right -->
            <div class="column is one-fourth">
              <transition name="fade" mode="out-in" appear>
                <div style="transition-delay: 2s">
                  <div v-tilt="tiltOptions">
                    <div class="box has-text-centered has-background-primary">
                      <img src="@/assets/black.png" alt="Logo" style="width:200px;">
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
      }
    }
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

</style>
