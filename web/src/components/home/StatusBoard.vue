<template>
  <div class="has-text-black-ter">

    <div class="box has-text-centered has-background-primary"
    style="border: 0px solid black">
      <img src="@/assets/black.png"
      alt="Logo"
      style="width:150px; opacity: 0.7;"
      @click="updateStatusData(); updateCallCountsData();"
      >
    </div>


    <!-- API status: 👌 ☠️ -->

    <div class="columns">
      <div class="column">
        <table>
          <tr>
            <th class="has-text-success">Names spied on:</th>
          </tr>
          <tr>
            <td>Total</td>
            <td>
              <label v-if="call_counts['counts']['total']">
                {{  call_counts['counts']['total']  }}
              </label>
              <label v-else class="loader"></label>
            </td>
          </tr>
          <tr>
            <td>Last 30 d</td>
            <td>
              <label v-if="call_counts['counts']['last30days']">
                {{  call_counts['counts']['last30days']  }}
              </label>
              <label v-else class="loader"></label>
            </td>
          </tr>
          <tr>
            <td>Last 24 hr</td>
            <td>
              <label v-if="call_counts['counts']['last24hours'] || call_counts['counts']['last24hours'] === 0">
                {{  call_counts['counts']['last24hours']  }}
              </label>
              <label v-else class="loader"></label>
            </td>
          </tr>
        </table>
      </div>

      <div class="column">
        <table>
          <tr>
            <th class="has-text-success">API status:</th>
          </tr>
          <tr>
            <td>Gateway</td>
            <td>
              <label v-if="statusEmoji('gateway')">
                {{statusEmoji('gateway')}}
              </label>
              <label v-else class="loader"></label>
            </td>
          </tr>
          <tr>
            <td>Webscore</td>
            <td>
              <label v-if="statusEmoji('webscore')">
                {{statusEmoji('webscore')}}
              </label>
              <label v-else class="loader"></label>
            </td>
          </tr>
          <tr>
            <td>Jobtitle</td>
            <td>
              <label v-if="statusEmoji('jobtitle')">
                {{statusEmoji('jobtitle')}}
              </label>
              <label v-else class="loader"></label>
            </td>
          </tr>
        </table>
      </div>
    </div>

  </div>
</template>

<script>

import axios from 'axios'

export default {
  name: 'StatusBoard',
  components: {
  },

  data() {
    return {
      system_status: {
        'urls': {
          'gateway': 'https://backend-mu7u3ykctq-lz.a.run.app/server_status/gateway_status',
          'webscore': 'https://backend-mu7u3ykctq-lz.a.run.app/server_status/webscore_status',
          'jobtitle': 'https://backend-mu7u3ykctq-lz.a.run.app/server_status/jobtitle_status',
        },
        'status': {
          'gateway': undefined,
          'webscore': undefined,
          'jobtitle': undefined,
        }
      },

      call_counts: {
        'url': 'https://backend-mu7u3ykctq-lz.a.run.app/db_routes/api_calls_count',
        'counts': {
          'total': undefined,
          'last30days': undefined,
          'last24hours': undefined
        }
      }

    }
  },

  methods: {

    // map status to what is being shown on the front end
    statusEmoji(endpoint) {
      if (this.system_status['status'][endpoint] == undefined) {
        return false
      } else if (this.system_status['status'][endpoint] == true) {
        return '👌'
      } else if  (this.system_status['status'][endpoint] == false) {
        return '☠️'
      } else {
        return '☠️'
      }
    },

    updateStatusData() {

      var vm = this

      // clean current statuses
      for (let key in this.system_status['status']){
        this.system_status['status'][key] = undefined
      }

      // for the sake of simplicity lets not do this in a loop
      // do each call separately

      // gateway
      axios.get(vm.system_status['urls']['gateway'])
      .then(response => {
        vm.system_status['status']['gateway'] = response['data']['is_up']
      }).catch(error => {
        console.log(JSON.stringify(error))
        vm.system_status['status']['gateway'] = false
      })

      // webscore
      axios.get(vm.system_status['urls']['webscore'])
      .then(response => {
        vm.system_status['status']['webscore'] = response['data']['is_up']
      }).catch(error => {
        console.log(JSON.stringify(error))
        vm.system_status['status']['webscore'] = false
      })

      // gateway
      axios.get(vm.system_status['urls']['jobtitle'])
      .then(response => {
        vm.system_status['status']['jobtitle'] = response['data']['is_up']
      }).catch(error => {
        console.log(JSON.stringify(error))
        vm.system_status['status']['jobtitle'] = false
      })
    },

    updateCallCountsData() {

      var vm = this

      // clean current counts
      for (let key in this.call_counts['counts']){
        this.call_counts['counts'][key] = undefined
      }

      // create dates to filter on
      let date = new Date()
      let last30days = new Date(new Date().setDate(date.getDate() - 30))
      let last24hours = new Date(new Date().setDate(date.getDate() - 1))

      // make mongo filters
      let filters = {
        'total': {},
        'last30days': {'time': {'$gte': last30days.toISOString()}},
        'last24hours': {'time': {'$gte': last24hours.toISOString()}}
      }

      // same as with updateStatusData
      // for the sake of simplicity lets not do this in a loop
      // do each call separately

      // total
      axios.get(vm.call_counts['url'], {
        params: {
          filter: JSON.stringify(filters['total'])
        }
      })
      .then(response => {
        vm.call_counts['counts']['total'] = response['data']
      }).catch(error => {
        console.log(JSON.stringify(error))
        vm.call_counts['counts']['total'] = '☠️'
      })

      // last30days
      axios.get(vm.call_counts['url'], {
        params: {
          filter: JSON.stringify(filters['last30days'])
        }
      })
      .then(response => {
        vm.call_counts['counts']['last30days'] = response['data']
      }).catch(error => {
        console.log(JSON.stringify(error))
        vm.call_counts['counts']['last30days'] = '☠️'
      })

      // last24hours
      axios.get(vm.call_counts['url'], {
        params: {
          filter: JSON.stringify(filters['last24hours'])
        }
      })
      .then(response => {
        vm.call_counts['counts']['last24hours'] = response['data']
      }).catch(error => {
        console.log(JSON.stringify(error))
        vm.call_counts['counts']['last24hours'] = '☠️'
      })
    }
  },

  mounted() {
    this.updateStatusData()
    this.updateCallCountsData()
  }

}
</script>

<style scoped>

/* Spinnig Icon */
.loader {
  display: inline-flex;
  border: 3px solid #8338EC;
  border-top: 3px solid #FF1279; /* Blue */
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
