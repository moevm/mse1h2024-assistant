<script>
import {instance} from "@/main.js";
import async from "async";
import {post_request} from "@/requests";
export default {
  name: 'Chat',
  methods: {
    restart(){
      this.$router.push('/');
    },
    send_text(){
      let message_window = document.getElementById("message_window")
      this.append_message(message_window.value)
      post_request(Number(this.$store.getters.getState.course),
          this.$store.getters.getState.subject,
          document.getElementById("message_window").value)
          .then(res => this.append_message(res))
      message_window.value = ""
    },
    open_voice(){
      document.getElementById("text_interface").hidden = true
      document.getElementById("voice_interface").hidden = false
    },
    send_voice(){

      //Удалить
      this.append_message("Голосовое отправлено")
      //Удалить

      this.close_voice()
      post_request(Number(this.$store.getters.getState.course),
          this.$store.getters.getState.subject,
          document.getElementById("message_window").value)
          .then(res => this.append_message(res))
    },
    delete_voice(){
      this.close_voice()
    },
    close_voice(){
      document.getElementById("text_interface").hidden = false
      document.getElementById("voice_interface").hidden = true
    },
    append_message(message){
      let log = document.getElementById("message_log")
      let li = document.createElement("li")
      li.appendChild(document.createTextNode(message))
      log.appendChild(li)
    }
  }
}
</script>

<template>
  <ul id="message_log"></ul>
  <div id="text_interface">
    <input id="message_window" type="text">
    <button @click="send_text">отправить</button>
    <button @click="open_voice">голосовое</button>
  </div>

  <div id="voice_interface" hidden="true">
    <p>---график гс---</p>
    <button @click="send_voice">отправить</button>
    <button @click="delete_voice">удалить</button>
  </div>

  <button @click="restart">Перезапуск</button>
</template>

<style scoped lang="scss">

</style>