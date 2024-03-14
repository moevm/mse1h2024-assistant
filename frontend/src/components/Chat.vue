<template>
  <v-row align="center" justify="center">
    <v-card id="chat" style="box-shadow: none">
      <v-card-text id="messages" style="padding: 0">
        <v-list-item v-for="(message, index) in messages" :key="index">
            <v-list-item-title :class="message.me ? 'text-right' : 'text-left'">
              <v-chip :color="message.me ? 'primary' : ''">{{ message.content }}</v-chip>
              <v-list-item-subtitle>{{ message.created_at }}</v-list-item-subtitle>
            </v-list-item-title>
        </v-list-item>
      </v-card-text>

      <v-card-actions style="padding: 0; justify-content: space-between">
        <v-text-field v-show="text_visible" v-model="newMessage" label="Сообщение" style="margin: 8px" hide-details></v-text-field>
        <v-btn class="button" v-show="send_text_visible" @click="send_message" color="primary" icon="mdi-send-variant-outline"></v-btn>
        <v-btn class="button" v-show="open_voice_visible" @click="open_voice" color="primary" style="margin: 0" icon="mdi-microphone-outline"></v-btn>
        <v-btn class="button" v-show="send_voice_visible" @click="send_voice" color="primary" icon="mdi-send-variant-outline"></v-btn>
        <v-btn class="button" v-show="delete_voice_visible" @click="delete_voice" color="primary" icon="mdi-delete-outline"></v-btn>
      </v-card-actions>
    </v-card>
  </v-row>

  <v-btn id="restart-button" class="button" @click="restart" icon="mdi-refresh"></v-btn>
</template>

<script>
import {post_request} from "@/requests"

export default {
  data() {
    return {
      text_visible: true,
      send_text_visible: true,
      open_voice_visible: true,
      send_voice_visible: false,
      delete_voice_visible: false,
      messages: [
        { content: 'Привет, чем могу помочь?', me: false, created_at: this.get_date() },
      ],
      newMessage: ''
    }
  },

  methods: {
    create_message(content, is_me) {
      this.messages.unshift({
        content: content,
        me: is_me,
        created_at: this.get_date()
      })
    },
    get_date(){
      let currentTime = new Date();
      let hours = currentTime.getHours();
      let minutes = currentTime.getMinutes();

      if (minutes < 10) {
        minutes = "0" + minutes;
      }

      return hours + ":" + minutes;
    },
    send_message() {
      if (this.newMessage.trim() !== '') {
        this.create_message(this.newMessage, true)
        post_request(Number(this.$store.getters.getState.course),
            this.$store.getters.getState.subject, this.newMessage)
            .then(res => this.create_message(res, false))
        this.newMessage = '';
      }
    },

    restart() {
      this.$router.push('/');
    },

    open_voice() {
      this.text_visible = false
      this.send_text_visible = false
      this.open_voice_visible = false

      this.send_voice_visible = true
      this.delete_voice_visible = true
    },

    close_voice() {
      this.text_visible = true
      this.send_text_visible = true
      this.open_voice_visible = true

      this.send_voice_visible = false
      this.delete_voice_visible = false
    },

    send_voice() {

      //Переделать
      this.create_message("Голосовое отправлено", true)
      this.close_voice()
      post_request(Number(this.$store.getters.getState.course),
          this.$store.getters.getState.subject,
          "Голосовое отправлено")
          .then(res => this.create_message(res, false))
      //Передалать
    },

    delete_voice() {
      this.close_voice()
    },
  }
}
</script>

<style scoped>

#chat {
  position: relative;
  background: none;
  width: 45%;
  height: 93vh;
}
#messages {
  height: 80%;
  overflow-y: auto;
  display: flex;
  flex-direction: column-reverse;
}

#restart-button{
  position: fixed;
  margin: 10px;
  top: 0;
  right: 0;
  background-color: transparent;

}

</style>