<template>
  <div class="indexNav">
      <el-row :gutter="10">
      <el-col :span="6">
        <div class="grid-content bg-purple">
          <img src="../../../static/img/icon/icon10.png">
          <br>
          蔬菜
        </div>
      </el-col>
      <el-col :span="6">
        <div class="grid-content bg-purple">
          <img src="../../../static/img/icon/icon3.png"><br>
          水果
        </div>
      </el-col>
      <el-col :span="6">
        <div class="grid-content bg-purple">
          <img src="../../../static/img/icon/icon9.png"><br>
          鲜肉
        </div>
      </el-col>
      <el-col :span="6">
        <div class="grid-content bg-purple">
          <img src="../../../static/img/icon/icon8.png"><br>
          水产
        </div>
      </el-col>
    </el-row>


    <el-row :gutter="10">
      <el-col :span="6">
        <div class="grid-content bg-purple">
          <img src="../../../static/img/icon/icon7.png"><br>
          豆腐豆干
        </div>
      </el-col>
      <el-col :span="6">
        <div class="grid-content bg-purple">
          <img src="../../../static/img/icon/icon11.png"><br>
          粮油
        </div>
      </el-col>
      <el-col :span="6">
        <div class="grid-content bg-purple">
          <img src="../../../static/img/icon/icon12.png"><br>
          日化商品
        </div>
      </el-col>
      <el-col :span="6">
        <div class="grid-content bg-purple">
          <img src="../../../static/img/icon/icon13.png"><br>
          冻货
        </div>
      </el-col>
    </el-row>
    </div>
</template>

<script>
export default {
  name: "indexNav",
  data() {
    return {
    };
  },

  methods: {
    
  }
};
</script>


<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.grid-content {
  margin-top: 1px;
  height: 70px;
  font-size: 14px;
  text-align: center;
  padding: 3px;
}
.grid-content img {
  max-width:40px ;
}
</style>