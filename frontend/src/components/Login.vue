<template>
  <p>Выберите курс</p>
  <select id="course" name="course">
    <option value="course1">1</option>
    <option value="course2">2</option>
  </select>
  <p>Выберите предмет</p>
  <select id="subject" name="subject">
    <option value="subject1">Программирование</option>
    <option value="subject2">Информатика</option>
  </select>
  <button @click="start">Начать</button>
</template>

<script>
export default {
  name: 'Login',
  methods: {
    start(){
      this.$store.commit('setCourse', document.getElementById("course").options[document.getElementById("course").selectedIndex].text)
      this.$store.commit('setSubject', document.getElementById("subject").options[document.getElementById("subject").selectedIndex].text)
      console.log(this.$store.getters.getState)
      this.$router.push('/chat');
    }
  }
}
</script>

<style scoped lang="scss">

</style>
