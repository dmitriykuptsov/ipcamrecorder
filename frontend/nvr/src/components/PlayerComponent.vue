<template>
  <div class="video-player">
    <h3 style="width: 100%">
      Camera archive
    </h3>
    <div>
      <video ref="video" width="1200" height="600" controls preload=none></video>
    </div>
    <div style="margin-top: 10px; width: 100%;">
      <table style="width: 600px; margin: auto;">
        <tr style="width: 600px">
          <td>
            <button style="margin-right: 10px; display:inline;" class="btn btn-dark btn-lg btn-block btn-add" @click="decrementTime">
              &lt;
            </button>
          </td>
          <td>
            <VueCtkDateTimePicker :minDate="minDate.toLocaleString()" :maxDate="maxDate.toLocaleString()" v-model="refTime" v-on:is-hidden="onRefTimeChanged"></VueCtkDateTimePicker>
          </td>
          <td>
            <button style="margin-left: 10px; display:inline;" class="btn btn-dark btn-lg btn-block btn-add" @click="incrementTime">
              &gt;
            </button>
          </td>
        </tr>
      </table>
      <div class="timerange">`
        Possible video search ranges (MIN: {{new Date(rangeMin * 1000).toLocaleString()}} &nbsp; &nbsp; MAX: {{new Date(rangeMax * 1000).toLocaleString()}})
      </div>
    </div>
  </div>
</template>

<script>

import Hls from 'hls.js';
import axios from "axios";
import VueCtkDateTimePicker from 'vue-ctk-date-time-picker';
import 'vue-ctk-date-time-picker/dist/vue-ctk-date-time-picker.css';


export default {
  data() {
    return {
      rangeMin: 0,
      rangeMax: 0,
      minDate :  new Date(this.rangeMin * 1000),
      maxDate :  new Date(this.rangeMax * 1000),
      refTimeSec: Math.floor(Date.now() / 1000),
      refTime: new Date(),
      step: 300
    }
  },
  methods: {
    onRefTimeChanged: function() {
      this.setTimestamp(() => {
        let hls = new Hls();
        let stream = this.$BASE_URL + "/api/get_next_m3u8/playlist.m3u8";
        let video = this.$refs["video"];
        hls.loadSource(stream);
        hls.attachMedia(video);
        hls.on(Hls.Events.MANIFEST_PARSED, function () {
          video.play();
        });
      })
    },
    pollTimeRanges: function () {
      const data = {  };
      const headers = {
        "Content-Type": "application/json",
      };
      axios
        .post(this.$BASE_URL + "/api/get_timestamp_range/", data, { headers })
        .then((response) => {
          if (response.data[1] == 200) {
            this.rangeMin = response.data[0].result.min;
            this.rangeMax = response.data[0].result.max;
          }
        });
    },
    setTimestamp(cb) {
      const data = {  };
      const headers = {
        "Content-Type": "application/json",
      };
      axios
        .post(this.$BASE_URL + "/api/set_timestamp/" + this.refTimeSec, data, { headers })
        .then((response) => {
          if (response.data[1] == 200) {
            cb()
          }
        }
      );
    },
    incrementTime() {
      this.refTimeSec = this.refTimeSec + this.step;
      this.refTime = new Date(this.refTimeSec * 1000);
      this.setTimestamp(() => {
        let hls = new Hls();
        let stream = this.$BASE_URL + "/api/get_next_m3u8/playlist.m3u8";
        let video = this.$refs["video"];
        hls.loadSource(stream);
        hls.attachMedia(video);
        hls.on(Hls.Events.MANIFEST_PARSED, function () {
          video.play();
        });
      })
    },
    decrementTime() {
      this.refTimeSec = this.refTimeSec - this.step;
      this.refTime = new Date(this.refTimeSec * 1000);
      this.setTimestamp(() => {
        let hls = new Hls();
        let stream = this.$BASE_URL + "/api/get_next_m3u8/playlist.m3u8";
        let video = this.$refs["video"];
        hls.loadSource(stream);
        hls.attachMedia(video);
        hls.on(Hls.Events.MANIFEST_PARSED, function () {
          video.play();
        });
      })
    }
  },
  mounted() {
    let hls = new Hls();
    let stream = this.$BASE_URL + "/api/get_next_m3u8/playlist.m3u8";
    let video = this.$refs["video"];
    hls.loadSource(stream);
    hls.attachMedia(video);
    hls.on(Hls.Events.MANIFEST_PARSED, function () {
      video.play();
    });
    let that = this;
    setInterval(function () {
       that.pollTimeRanges();
    }, 5000); 
  },
  components: {
    VueCtkDateTimePicker 
  }
};
</script>

<style scoped>

h3 {
  color: #372d69;
  text-align: center;
}

.video-player {
  width: 100%;
  height: 100%;
}

.timerange {
  margin-top: 10px;
  color: #372d69;
  font-weight: bold;
}
</style>
