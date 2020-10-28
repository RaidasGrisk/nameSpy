<template>
  <div class="section" style="margin-left: auto; margin-right: auto;">

    <Service/>

    <!-- <section class="section"> -->
      <!-- ExplainCard modals -->
      <!-- <div class="is-size-7">

        <Modal v-show="showModal_WebScore" @close="showModal_WebScore=false">
          <ExplainCardWebScore/>
        </Modal>
        <Modal v-show="showModal_Occupation" @close="showModal_Occupation=false">
          <ExplainCardOccupation/>
        </Modal>

        <div @click="showModal_WebScore=true">
          <a class="has-text-weight-bold has-text-success">web score</a>
        </div>

        <div @click="showModal_Occupation=true">
          <a class="has-text-weight-bold has-text-success">occupation</a>
        </div>
      </div>
    </section> -->

  </div>
</template>

<script>

// import ExplainCardWebScore from '@/components/docs/ExplainCardWebScore'
// import ExplainCardOccupation from '@/components/docs/ExplainCardOccupation'

// import Modal from '@/components/Modal'
import Service from '@/components/home/Service'


export default {

  name: 'Home',

  components: {
    // ExplainCardWebScore,
    // ExplainCardOccupation,
    // Modal,
    Service
  },

  data() {
    return {
    }
  },

  mounted() {

    // here is the bug I'm experiencing:
    // a chart inside a modal is not being rendered initially.
    // It renders if I resize browser zoom level. Many such issues on google,
    // yet none of the solutions work for vue-trend-chart package.
    // Therefore here is a fix:
    // initially inside the data component "showModal_WebScore: true"
    // Then here I set it to false when mounted and it fixes the bug for some reason (?)
    this.showModal_WebScore = false

  }
}

</script>

<style>


</style>
