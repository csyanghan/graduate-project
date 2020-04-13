<template>
  <h1>Hello {{ username }} !</h1>
</template>

<script>
import { mapGetters } from 'vuex';

export default {
  name: 'UserInfo',
  computed: {
    ...mapGetters([
      'username',
    ]),
  },
};
</script>
