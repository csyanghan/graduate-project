<template>
  <div class="index-container" keep-alive>
    <div class="search">
      <h1>案例推荐</h1>
      <el-input placeholder="请输入内容" v-model="searchKeyword" class="search-input" @keyup.enter.native="handleSearch">
        <el-button slot="append" icon="el-icon-search" @click="handleSearch"></el-button>
      </el-input>
    </div>
    <div class="search-list">
      <div class="loading" v-if="loading">
        <pacman-loader :loading="loading" color="#409EFF"></pacman-loader>
        <div class="text">案例搜索中</div>
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
      <div v-if="searchResultList.length === 0 && searchResultLengthZero" style="display:flex; flex-direction:column; align-items: center; padding: 24px 0;">
        <i class="el-icon-search"/>
        <div style="margin-top:24px">暂没有搜索结果</div>
      </div>
    </div>
    <div class="search-list">
      <div class="recommend">
        <h3 v-if="username">和你有共同喜好的人也爱看:</h3>
        <h3 v-else>大家都爱看:</h3>
      </div>
      <el-row :gutter="24" v-if="recommendList.length > 0">
        <el-col :span="8" v-for="law in recommendList" :key="law.id">
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
      <div v-else style="text-align:center; margin-top: 100px">暂无推荐,随便看看吧!</div>
    </div>

    <div class="search-list" style="margin-top:24px" v-if="recommendByItemList.length > 0">
      <div class="recommend">
        <h3>猜你喜欢:</h3>
      </div>
      <el-row :gutter="24">
        <el-col :span="8" v-for="law in recommendByItemList" :key="law.id">
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
import { mapGetters } from 'vuex';

export default {
  name: 'Index',
  data() {
    return {
      searchKeyword: '',
      searchResultList: [],
      totalListLength: 0,
      loading: false,
      time: 0,
      recommendList: [],
      recommendByItemList: [],
      searchResultLengthZero: false,
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
    ...mapGetters([
      'username',
    ]),
  },
  watch: {
    username() {
      this.getRecommendLaw();
      this.getRecommendLawByItem();
    },
  },
  methods: {
    handleSearch() {
      this.loading = true;
      this.searchResultList = [];
      this.totalListLength = 0;
      this.searchResultLengthZero = false;
      this.$http.post('/api/law/search', {
        keyword: this.searchKeyword,
      }).then((res) => {
        this.searchResultList = res.data.data;
        this.totalListLength = res.data.length;
        this.loading = false;
        this.time = res.data.time;
        this.searchResultLengthZero = true;
      });
    },
    linkTo(id) {
      return `/detail/${id}`;
    },
    getRecommendLaw() {
      this.$http.get('/api/law/recommend').then((res) => {
        this.recommendList = res.data.data.slice(0, 9);
      });
    },
    getRecommendLawByItem() {
      this.$http.get('/api/law/recommendByItem').then((res) => {
        this.recommendByItemList = res.data.data;
      });
    },
  },
  mounted() {
    this.getRecommendLaw();
    this.getRecommendLawByItem();
  },
};
</script>

<style lang="less">
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
  height: 68px;
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
