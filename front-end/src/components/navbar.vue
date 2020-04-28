<template>
  <div class="gp-navbar">
    <img src="@/assets/logo.svg" @click="goToIndex"/>
    <div class="left-nav">
      <div v-if="!username">
        <el-button type="text" @click="login">登录</el-button>
        <el-button type="text" @click="register">注册</el-button>
      </div>
      <el-dropdown v-if="username" @command="handleClick">
        <span class="el-dropdown-link">
          {{ username }}<i class="el-icon-arrow-down el-icon--right"></i>
        </span>
        <el-dropdown-menu slot="dropdown">
          <el-dropdown-item command="user-info">基本信息</el-dropdown-item>
          <el-dropdown-item command="message">消息通知</el-dropdown-item>
          <el-dropdown-item command="logout">注销</el-dropdown-item>
        </el-dropdown-menu>
      </el-dropdown>
    </div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex';
import Cookies from 'js-cookie';

export default {
  name: 'NavBar',
  methods: {
    login() {
      this.$router.push({ path: '/login' });
    },
    register() {
      this.$router.push({ path: '/register' });
    },
    goToIndex() {
      this.$router.push({ path: '/' });
    },
    handleClick(command) {
      if (command === 'logout') {
        this.$store.commit('userLogin', {
          userInfo: {},
        });
        Cookies.remove('userId');
      }
      if (command === 'user-info') this.$router.push({ path: '/user-info' });
      if (command === 'message') this.$router.push({ path: '/message' });
    },
  },
  computed: {
    ...mapGetters([
      'username',
    ]),
  },
};
</script>

<style lang="less">
.el-dropdown-link {
  cursor: pointer;
  color: #409EFF;
}
.el-icon-arrow-down {
  font-size: 12px;
}

.gp-navbar {
  padding-right: 20px;
  width: 1140px;
  display: flex;
  justify-content: space-between;
  border-bottom: 1px solid #dcdfe6;
  margin: 0 auto;
  align-items: center;
  height: 80px;
  img {
    cursor: pointer;
    user-select: none;
  }
}
</style>
