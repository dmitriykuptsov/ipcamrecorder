<template>
  <div class="video-player">
    <video width="352" height="198" controls>
        <source src="/api/get_next_m3u8/playlist.m3u8" type="application/x-mpegURL">
    </video>
  </div>
</template>

<script>

export default {
  name: "PlayerComponent",
  data() {
    return {
    };
  },
  methods: {
  },
  components: {
  },
};
</script>

<style scoped>
.video-player {
    width: 100%;
    height: 90%;
}
</style>
