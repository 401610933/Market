<template>
  <div class="top">
    <el-row :gutter="2">
  <el-col :span="7">
      <el-avatar class="top-left"><img src="/static/img/logo.png"></el-avatar>
  <el-dropdown>
      <span class="el-dropdown-link">
        <i class="el-icon-arrow-down el-icon--right"></i>
      </span>
      <el-dropdown-menu slot="dropdown">
        <!-- <el-dropdown-item disabled>禁止显示</el-dropdown-item> -->
        <!-- <el-dropdown-item divided>天生上品生鲜集市</el-dropdown-item> -->
        <el-dropdown-item>天生上品生鲜集市</el-dropdown-item>
      </el-dropdown-menu>
    </el-dropdown>
  </span></el-col>

  <el-col :span="17">
    <el-input class="input" prefix-icon="el-icon-search" v-on:focus="thisclick" placeholder="搜索商品"></el-input>
  </el-col>
</el-row>

    
    
  </div>
</template>

<script>
export default {
  name: "top",
  data() {
    return {};
  },
  methods: {
    thisclick:function(){
      this.$router.push({path:'search'})
    }
  }
};
</script>


<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.top {margin-top:5px;}
.top-left img {
 max-width: 40px; max-height: 40px;
}
.el-dropdown-link {
  cursor: pointer;
}
.el-icon-arrow-down {
  font-size: 16px;
  font-weight: bold;
}
.input {box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1)}
</style>
