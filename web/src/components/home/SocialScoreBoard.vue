<template>
  <section class="section">
    <div class="columns is-centered">
      <div class="box column is-narrow">
        <div class="table-container">
        <table class="table is-narrow is-fullwidth" style="font-size: 10px !important;">
          <thead>
            <th v-for="key in gridColumns()" :key="key">
              {{ key }}
            </th>
          </thead>
          <tfoot>
          </tfoot>
          <tbody>
            <!-- iter over entry and idx, to dodge vue warn of using non-primitive value as key -->
            <tr v-for="(entry, idx) in gridData" :key="idx">
              <td v-for="key in gridColumns()" :key="key" :class="entry['class']">
                {{ entry[key] }}
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      </div>
    </div>
  </section>
</template>

<script>
export default {
  name: 'SocialScoreBoard',
  props: {
    gridData: Array
  },

  data() {
    return {

    }
  },

  methods: {
    gridColumns() {
      return Object.keys(this.gridData[0])

    }
  },

  // watch: {
  //   newDataRow: {
  //     // the callback will be called immediately after the start of the observation
  //     immediate: true,
  //     handler () {
  //       if ('input' in this.newDataRow) {
  //         var newRow = {'person': this.newDataRow['input'], 'google_items': 1, 'wiki_items': 0, 'twtr_users': 1, 'twtr_followers': 3, 'ig_users': 0, 'ig_followers': 0}
  //         this.gridData.push(newRow)
  //       }
  //     }
  //   }
  // }

}
</script>

<style scoped>

</style>
