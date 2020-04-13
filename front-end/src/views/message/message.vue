<template>
  <h1>Hello {{ username }} ! 你没有未读的消息 ！！</h1>
</template>

<script>
import { mapGetters } from 'vuex';

export default {
  name: 'Message',
  computed: {
    ...mapGetters([
      'username',
    ]),
  },
};
</script>
