<template>
  <div class="gp-login">
    <h2>用户登录</h2>
    <el-form ref="loginForm" :model="loginForm" label-width="80px">
      <el-form-item label="用户名">
        <el-input v-model="loginForm.username"></el-input>
      </el-form-item>
      <el-form-item label="密码">
        <el-input v-model="loginForm.password" type="password"></el-input>
      </el-form-item>
      <el-form-item class="gp-bottom">
        <el-button type="primary" @click="onSubmit">登录</el-button>
        <el-button class="register-btn" @click="register">去注册</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
export default {
  name: 'Login',
  data() {
    return {
      loginForm: {
        username: '',
        password: '',
      },
    };
  },
  methods: {
    onSubmit() {
      this.$http.post('/api/user/login', {
        username: this.loginForm.username,
        password: this.loginForm.password,
      }).then((res) => {
        if (res.data.code === 200) {
          this.$message({
            message: '登录成功',
            type: 'success',
          });
          this.$router.push({ path: '/' });
          this.$store.commit('userLogin', {
            userInfo: res.data.data,
          });
        } else {
          this.$message({
            message: res.data.msg,
            type: 'error',
          });
        }
      });
    },
    register() {
      this.$router.push({ path: '/register' });
    },
  },
};
</script>

<style lang="less" scoped>
.gp-login {
  width: 46%;
  margin: 100px auto;
  h2 {
    text-align: center;
    margin-bottom: 28px;
  }
  .gp-bottom {
    .el-button {
      width: 120px;
    }
    display: flex;
    justify-content: space-around;
    .register-btn {
      margin-left: 80px;
    }
  }
}
</style>
