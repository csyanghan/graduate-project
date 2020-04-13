<template>
  <div class="gp-register">
    <h2>用户注册</h2>
    <el-form ref="registerForm" :model="registerForm" label-width="80px">
      <el-form-item label="用户名">
        <el-input v-model="registerForm.username"></el-input>
      </el-form-item>
      <el-form-item label="密码">
        <el-input v-model="registerForm.password" type="password"></el-input>
      </el-form-item>
      <el-form-item class="gp-bottom">
        <el-button type="primary" @click="onSubmit">注册</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
export default {
  name: 'Register',
  data() {
    return {
      registerForm: {
        username: '',
        password: '',
      },
    };
  },
  methods: {
    onSubmit() {
      this.$http.post('/user/register', {
        username: this.registerForm.username,
        password: this.registerForm.password,
      }).then((res) => {
        if (res.data.code === 200) {
          this.$message({
            message: '注册成功',
            type: 'success',
          });
          this.$router.push({ path: '/' });
        } else {
          this.$message({
            message: '用户名已存在',
            type: 'error',
          });
        }
      });
    },
  },
};
</script>

<style lang="less" scoped>
.gp-register {
  width: 46%;
  margin: 100px auto;
  h2 {
    text-align: center;
    margin-bottom: 28px;
  }
  .gp-bottom {
    /deep/ .el-form-item__content {
      margin-left: 0 !important;
    }
    .el-button {
      width: 120px;
    }
    display: flex;
    justify-content: center;
  }
}
</style>
