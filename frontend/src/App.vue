<template>
  <div class="app">
    <div class="logo">
      Assistant
    </div>
    <div id="nav">
      <router-link to="/"></router-link>
    </div>
    <router-view/>
    <v-btn
      id="help_btn"
      class="button"
      @click="help"
      icon="mdi-help"
    />
  </div>
  
</template>

<script>
export default {
  name: 'App',
  methods: {
    help(){
      alert("Help");
    }
  }
}
</script>

<style lang="scss">
.app{
  background: rgb(194,191,255);
  background: linear-gradient(90deg, rgba(194,191,255,1) 0%, rgba(215,212,255,1) 10%, rgba(237,235,255,1) 30%, rgba(255,255,255,1) 50%, rgba(237,235,255,1) 70%, rgba(215,212,255,1) 90%, rgba(194,191,255,1) 100%);
  height: 100vh;
}
.logo{
  font-family: fantasy;
  font-size: 30px;
  padding-left: 10px;
}
#help_btn{
  position: fixed;
  bottom: 0;
  right: 0;
  margin: 10px;
  background-color: transparent;
}

.button:hover {
  transform: scale(1.1);
}

</style>
