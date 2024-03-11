<template>
  <div>
    <v-card class="login_card">
      <v-select
        label="Выберите номер курса"
        :items="['1', '2', '3', '4', '5', '6']"
        variant="outlined"
        v-model="course"
      />
      <v-select
        label="Выберите предмет"
        :items="['Программирование', 'Информатика']"
        variant="outlined"
        :disabled="this.course.length < 1"
        v-model="subject"
      />
      <v-btn 
        @click="start" 
        class="login_btn"
        :disabled="this.subject.length < 1 || this.course.length < 1"
      >
        Начать
      </v-btn>
    </v-card>
  </div>
</template>

<script>
export default {
  name: 'Login',
  data:() => {
    return {
      course: '',
      subject: ''
    }
  },
  methods: {
    start(){
      this.$store.commit('setCourse', this.course);
      this.$store.commit('setSubject', this.subject);
      console.log(this.$store.getters.getState)
      this.$router.push('/chat');
    }
  }
}
</script>

<style scoped lang="scss">
.login_card{
    width: 15%;
    padding: 30px;
    margin: auto;
    background-color: $card-bcg-color;
    text-align: center;
}
.login_btn{
  background-color: $login-btn-color;
  width: 50%;
  font-weight: bold;
}
</style>
