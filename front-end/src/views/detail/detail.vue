<template>
  <div class="detail">
    <h1> {{ lawDetail.anming }}</h1>
    <div class="sub-contanier">
      <div>
        <span class="sub-detail">案由: {{ lawDetail.anyou }}</span>
        <span class="sub-detail"> 案件类型: {{ lawDetail.anjianleixin }}</span>
      </div>
      <div>
        <span class="sub-detail">审理程序: {{ lawDetail.shenlichenxu || '暂无'  }}</span>
        <span class="sub-detail">审理法院: {{ lawDetail.shenlifayuan }}</span>
      </div>
    </div>
    <div class="judge">
      <h3 v-if="lawDetail.anqinzaiyao">案情摘要:</h3>
      <p v-html="lawDetail.anqinzaiyao" v-if="lawDetail.anqinzaiyao"></p>
      <h3 style="margin-top: 12px">裁判要点:</h3>
      <p>{{ lawDetail.caipanyaodian }}</p>
    </div>

    <h3 style="margin-top: 24px">相似案例推荐:</h3>
    <el-row :gutter="24">
        <el-col :span="8" v-for="law in recommendList" :key="law.anming">
          <el-card class="gp-card">
            <div slot="header" class="card-header">
              <router-link :to="linkTo(law.id)"> {{ law.anming }}</router-link>
            </div>
            <div class="card-body">
              {{ law.caipanyaodian }}
            </div>
          </el-card>
        </el-col>
      </el-row>
  </div>
</template>

<script>
import { mapGetters } from 'vuex';

export default {
  name: 'Detail',
  data() {
    return {
      lawDetail: {},
      recommendList: [],
    };
  },
  computed: {
    lawid() {
      return this.$route.params.id;
    },
    ...mapGetters([
      'id',
    ]),
  },
  watch: {
    lawid(newVal) {
      if (newVal) this.getDetail(newVal);
    },
  },
  methods: {
    linkTo(id) {
      return `/detail/${id}`;
    },
    getDetail() {
      const params = {
        id: this.lawid,
      };
      if (this.id) params.userId = this.id;
      this.$http.get('/api/law/getLawById', {
        params,
      }).then((res) => {
        this.lawDetail = res.data.data;
        this.recommendList = res.data.data.recommend.filter((item) => item.anming !== this.lawDetail.anming);
      });
    },
  },
  mounted() {
    this.getDetail();
  },
};
</script>

<style lang="less" scoped>
.detail {
  h1 {
    text-align: center;
  }
  .sub-contanier {
    padding: 24px 0 24px 12px;
    .sub-detail {
      display: inline-block;
      height: 36px;
      line-height: 36px;
      width: 300px;
    }
  }
  .judge {
    padding: 0 0 0 12px;
    h3 {
      margin-bottom: 8px;
    }
    p {
      text-indent: 2em;
    }
  }
}
</style>
