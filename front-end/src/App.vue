<template>
  <el-container id="app">
    <el-header  height="80px">
      <nav-bar />
    </el-header>
    <el-main class="gp-main">
      <div class="main-content">
        <keep-alive>
          <router-view v-if="$route.meta.keepAlive"/>
        </keep-alive>
        <router-view v-if="!$route.meta.keepAlive"/>
      </div>
    </el-main>
    <el-footer class="gp-footer">
      Copyright © <el-link href="https://github.com/Ctum" target="_blank">Hanyang</el-link>
    </el-footer>
  </el-container>
</template>

<script>
import NavBar from '@/components/navbar.vue';

export default {
  name: 'App',
  components: {
    NavBar,
  },
  async mounted() {
    const res = await this.$http.get('/user/userInfo');
    if (res.data.code === 200) {
      this.$store.commit('userLogin', {
        userInfo: res.data.data,
      });
    }
  },
};
</script>
<style lang="less">
#app {
  font-family: "Helvetica Neue",Helvetica,"PingFang SC","Hiragino Sans GB","Microsoft YaHei","微软雅黑",Arial,sans-serif;
  position: relative;
  width: 100%;
  height: 100%;
  z-index: 1500;
  min-height: 100vh;
}
body {
  width: 100%;
}
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}
.main-content {
  margin: 0 auto;
  width: 1140px;
}
.gp-footer {
  display: flex;
  justify-content: center;
  align-items: center;
  color: #909399;
  font-size: 16px;
  span {
    color: #909399;
    font-size: 16px !important;
    margin-left: 4px;
  }
}
.gp-main {
  flex: 2;
}
</style>
