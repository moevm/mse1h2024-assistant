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
        @click="toggleHelpCard"
        icon="mdi-help"
    />

    <v-card v-show="helpCardVisible" id="help_card" class="help-card">
      <v-card-text>
        <div>
          <h2>Приветствую!</h2>
          <br>
          <p>Кафедральный ассистент поможет ответить на организационные вопросы.</p>
          <p>Для начала работы необходимо указать номер курса и интересующий Вас предмет.</p>
          <p>Далее вы можете отправить Ваш вопрос в текстовом или голосовом формате.</p>
          <p><strong>Ассистент может ошибаться.</strong></p>
          <p>Подумайте о том, чтобы проверить важную информацию.</p>
        </div>
      </v-card-text>
    </v-card>

  </div>
  
</template>

<script>
export default {
  name: 'App',

  data() {
    return {
      helpCardVisible: false
    };
  },

  mounted() {
    document.addEventListener('keydown', this.handleKeyPress);
  },
  beforeDestroy() {
    document.removeEventListener('keydown', this.handleKeyPress);
  },

  methods: {
    toggleHelpCard() {
      this.helpCardVisible = !this.helpCardVisible;
    },

    handleKeyPress(){
      this.helpCardVisible = false
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

#help_card{
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  max-width: 400px;
}

.help-card h2,p {
  text-align: center;
}


</style>
