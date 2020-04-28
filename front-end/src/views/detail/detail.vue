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
      <h3>裁判要点:</h3>
      <p>{{ lawDetail.caipanyaodian }}</p>
    </div>
  </div>
</template>

<script>

export default {
  name: 'Detail',
  data() {
    return {
      lawDetail: {},
    };
  },
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
    getDetail() {
      this.$http.get('/law/getLawById', {
        params: {
          id: this.id,
        },
      }).then((res) => {
        this.lawDetail = res.data.data;
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
