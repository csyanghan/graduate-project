<template>
  <h1>Detail- {{ id }}</h1>
</template>

<script>

export default {
  name: 'Detail',
  computed: {
    id() {
      return this.$route.params.id;
    },
  },
  watch: {
    id(newVal) {
      if (newVal) this.getDetail(newVal);
    },
  },
  methods: {
    getDetail(id) {
      //
      console.log(id);
    },
  },
};
</script>
