<template>
  <div class="hello">
    <h1 v-on:click="greet">{{ msg }}</h1>
    <h2>我的Vue</h2>
    <ul>
      <el-input-number v-model="num" @change="handleChange" :min="1" :max="10" label="描述文字"></el-input-number>
    </ul>
  </div>
</template>

<script>
export default {
  name: "HelloWorld",
  created() {
    // console.log(000);
    this.$axios
      .get("http://wx.zaiyi023.com/API/vue_api.php", {
        params: {
          Id: "11",
          flag: "open"
        }
      })
      .then(response => {
        // console.log("log=", response);
        console.log(response.data);
        this.msg = response.data;
      })
      .catch(response => {
        console.los("log=", response);
      });
  },
  data() {
    return {
      msg: "载入中",
      danxuan: "3",
      num:1
    };
  },

  methods: {
    greet: function() {
      alert(this.msg);
    },
    handleChange(value) {
        console.log(value);
      }
  }
};
</script>


<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h1,
h2 {
  font-weight: normal;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>
