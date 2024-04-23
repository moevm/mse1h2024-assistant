<template>
  <div>
    <v-card class="login_card" >
      <v-select
        label="Выберите номер курса"
        :items="courses"
        variant="outlined"
        v-model="course"
      />
      <v-select
        label="Выберите раздел"
        :items="subjects"
        variant="outlined"
        :disabled="this.course.length < 1"
        v-model="subject"
      />
      <v-btn
        @click="start"
        class="login_btn, button"
        :disabled="this.subject === '' || this.course === ''"
        data-testid="start-test"
      >
        Начать
      </v-btn>
    </v-card>
  </div>
</template>

<script>
import {get_courses} from "@/requests";

export default {
  name: 'Login',
  data:() => {
    return {
      course: '',
      subject: '',
      courses: [],
      subjects: [],
      back_data: {}
    }
  },

  async mounted() {
    try {
      this.back_data = await get_courses();
      this.courses = Object.keys(this.back_data)
    } catch (error) {
      console.error('Ошибка при загрузке курсов:', error);
    }
  },

  watch: {
    course(newCourse) {
      this.subject = '';
      this.subjects = this.back_data[newCourse] || [];
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
  width: 35%;
  padding: 30px;
  margin: auto;
  background-color: transparent;
  text-align: center;
  box-shadow: none;
}
.login_btn{
  width: 50%;
  font-weight: bold;
  background-color: transparent;
}
</style>



