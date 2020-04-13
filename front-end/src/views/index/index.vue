<template>
  <div class="index-container" keep-alive>
    <div class="search">
      <h1>案例搜索</h1>
      <el-input placeholder="请输入内容" v-model="searchKeyword" class="search-input" @keyup.enter.native="handleSearch">
        <el-button slot="append" icon="el-icon-search" @click="handleSearch"></el-button>
      </el-input>
    </div>
    <div class="search-list">
      <div class="loading" v-if="loading">
        <pacman-loader :loading="loading" color="#409EFF"></pacman-loader>
        <div class="text">数据搜索中</div>
      </div>
      <h3 v-if="showSearchResultTitle">搜索结果: 花了 {{ time }} s {{ prompt }}</h3>
      <el-row :gutter="24">
        <el-col :span="8" v-for="law in searchResultList" :key="law.id">
          <el-card class="gp-card">
            <div slot="header" class="card-header">
              <router-link :to="linkTo(law.id)"> {{ law.name }}</router-link>
            </div>
            <div class="card-body">
              {{ law.caipanyaodian }}
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script>
// eslint-disable-next-line import/extensions
import PacmanLoader from 'vue-spinner/src/PacmanLoader';

export default {
  name: 'Index',
  data() {
    return {
      searchKeyword: '',
      searchResultList: [],
      totalListLength: 0,
      loading: false,
      time: 0,
    };
  },
  components: {
    PacmanLoader,
  },
  computed: {
    prompt() {
      if (this.totalListLength === this.searchResultList.length) return `找到了${this.totalListLength}条数据`;
      return `找到了${this.totalListLength}条数据，但只返回前${this.searchResultList.length}条`;
    },
    showSearchResultTitle() {
      return this.searchResultList.length > 0;
    },
  },
  methods: {
    handleSearch() {
      this.loading = true;
      this.searchResultList = [];
      this.totalListLength = 0;
      this.$http.post('/law/search', {
        keyword: this.searchKeyword,
      }).then((res) => {
        this.searchResultList = res.data.data;
        this.totalListLength = res.data.length;
        this.loading = false;
        this.time = res.data.time;
      });
    },
    linkTo(id) {
      return `/detail/${id}`;
    },
  },
};
</script>

<style lang="less" scoped>
.search {
  text-align: center;
  margin-bottom: 48px;
  h1 {
    font-weight: 400;
    margin: 20px 0;
  }
  .search-input {
    width: 720px;
    margin: 0 auto;
  }
}
.search-list {
  h3 {
    font-weight: 400;
  }
  .loading {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    margin: 24px;
    .text {
      margin-left: 64px;
      margin-top: 32px;
      color: #409EFF;
      font-size: 20px;
    }
  }
}
.gp-card {
  margin: 12px 12px;
}
.card-body {
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  height: 70px;
}
.card-header {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.custom-loading {
  width: 100px;
}
</style>
