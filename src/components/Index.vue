<template>
  <div class="index">
    <top />

    
    <banner />   <!-- banner -->
   
    <indexNew />  <!-- 新闻通知 -->

    <indexNav /> <!--banner下面的导航模块-->

    <indexIMG /> <!--图片热卖区-->

    <foot />
  </div>
</template>

<script>
import top from "globals/top";
import foot from "globals/foot";
import banner from "indexs/banner";
import indexNav from "indexs/indexNav";
import indexNew from "indexs/indexNew";
import indexIMG from "indexs/indexIMG";
export default {
  name: "index",
  data() {
    return {};
  },
  methods: {},
  components: {
    top: top,
    foot: foot,
    banner: banner,
    indexNav: indexNav,
    indexNew: indexNew,
    indexIMG: indexIMG
  }
};
</script>


<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

</style>
