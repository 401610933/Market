<template>
  <div class="indexIMG">
    <el-row>
      <el-col :span="24">
        <img src="../../../static/img/banner/index_banner1.png" />
      </el-col>
    </el-row>
    <el-row :gutter="5">
      <el-col :span="12">
        <div class="grid-content bg-purple">
          <img src="../../../static/img/banner/index_banner2.jpg" />
        </div>
      </el-col>
      <el-col :span="12">
        <div class="grid-content bg-purple right">
          <img src="../../../static/img/banner/index_banner3.jpg" />
        </div>
      </el-col>
    </el-row>
  </div>
</template>

<script>
export default {
  name: "indexIMG",
  data() {
    return {};
  },

  methods: {}
};
</script>


<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.right { text-align: right;}
</style>