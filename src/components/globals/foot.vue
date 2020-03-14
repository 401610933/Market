<template>
  <div class="foot">
    <div>
      <el-col :span="4">
        <router-link to="/" class="active_item" exact>
        <div class="grid-content bg-purple"><i class="iconfont iconshouye1"></i><br>首页</div>
        </router-link>
      </el-col>
      <el-col :span="5">
        <router-link to="product" class="active_item" exact>
        <div class="grid-content bg-purple"><i class="iconfont iconfenlei"></i><br>分类</div>
        </router-link>
      </el-col>
      <el-col :span="5">
        <router-link to="helloworld" class="active_item" exact>
        <div class="grid-content bg-purple-light"><i class="iconfont iconkafei"></i><br>看点</div>
        </router-link>
      </el-col>
      <el-col :span="5">
        <router-link to="search" class="active_item" exact>
        <div class="grid-content bg-purple"><i class="iconfont icongouwuche"></i><br>购物车</div>
        </router-link>
      </el-col>
      <el-col :span="5">
        <router-link to="/" class="active_item" exact>
        <div class="grid-content bg-purple-light"><i class="iconfont iconwodeqianfenleishouye"></i><br>我的</div>
        </router-link>
      </el-col>
    </div>
  </div>
</template>

<script>
export default {
  name: "foot",
  data() {
    return {};
  },
  methods: {}
};
</script>


<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.foot {
  border-top: 1px solid #f3f3f3;
  font-size: 12px;
  position: fixed;
  bottom: 0px;
  background: #ffffff;
  display: inline-block;
  width: 100%;
  margin-left: -8px;
  padding-right: 8px;
  height: 45px;
  padding-top:5px ;
  
}
.grid-content{
  color: #808080;
  text-align: center;
  line-height: 20px;
}
.grid-content i{
  font-size: 24px;
}

.active_item.router-link-active .grid-content{
        color: #FF9900;
    }
</style>
