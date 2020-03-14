<template>
  <div class="index">
    <h2>我是搜索页面</h2>
    <span v-on:click="back">返回</span>
  </div>
</template>

<script>
import top from "globals/top";
export default {
  name: "index",
  data() {
    return {};
  },
  methods: {
    back:function(){
      this.$router.go(-1)
    }
  },
  components: {
    'top': top
  }
}
</script>


<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
li {list-style: none;}
</style>
