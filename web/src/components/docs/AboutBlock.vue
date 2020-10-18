<template>
  <div>
    <div class="card is-hidden1">
      <div class="card-header"><p class="card-header-title">About</p></div>
      <div class="card-content">
        <div class="content">
          <div class="columns" style="font-size: 11px !important;">
            <div class="column">
              <ExplainCardWebScore/>
            </div>
            <div class="column">
              <ExplainCardOccupation/>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>

// import modal from '@/components/Modal'
import ExplainCardWebScore from '@/components/docs/ExplainCardWebScore'
import ExplainCardOccupation from '@/components/docs/ExplainCardOccupation'

export default {

  name: 'AboutBlock',

  components: {
    // modal,
    ExplainCardWebScore,
    ExplainCardOccupation
  }

}
</script>

<style scoped>
</style>
