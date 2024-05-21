<template>
  <v-row align="center" justify="center">
    <v-card id="chat" style="box-shadow: none">
      <v-card-text id="messages" style="padding: 0">
        <v-list-item v-for="(message, index) in messages" :key="index">
          <v-list-item-title style="height: max-content;" :class="message.me ? 'text-right' : 'text-left'">
            <v-chip :color="message.me ? 'primary' : ''" style="white-space: pre-wrap; display: inline-block; max-width: 40%; width: max-content;
             text-align: left; word-break: break-word; height: max-content; border-radius: 10px"> {{ message.content }} </v-chip>
            <v-list-item-subtitle>{{ message.created_at }}</v-list-item-subtitle>
          </v-list-item-title>
        </v-list-item>
      </v-card-text>



      <v-card-actions class="d-flex justify-center" style="padding: 0; margin-right: 8px; height: 72px;">
        <v-text-field data-testid="text-test" v-show="text_visible" v-model="newMessage" @keyup.enter="send_message" label="Сообщение" style="margin: 8px" hide-details></v-text-field>
        <v-btn data-testid="send-test" class="button" v-show="send_text_visible" @click="send_message" color="primary" icon="mdi-send-variant-outline"></v-btn>
        <v-btn data-testid="voice-test" class="button" v-show="open_voice_visible" @click="start_voice" color="primary" style="margin: 0" icon="mdi-microphone-outline"></v-btn>
        <p v-show="isRunning">Запись:</p><div id="indicator" v-show="isRunning">{{ formatTime }}</div>
        <audio v-show="player_visible" controls ref="audioPlayer" :src="audioSrc" type="audio/mpeg"></audio>
        <v-btn class="button" v-show="stop_voice_visible" @click="stop_voice" color="primary" style="margin: 0" icon="mdi-pause"></v-btn>
        <v-btn class="button" v-show="send_voice_visible" @click="send_voice" color="primary" icon="mdi-send-variant-outline"></v-btn>
        <v-btn class="button" v-show="delete_voice_visible" @click="delete_voice" color="primary" icon="mdi-delete-outline"></v-btn>
      </v-card-actions>
    </v-card>
  </v-row>

  <v-btn id="restart-button" class="button" @click="restart" icon="mdi-refresh"></v-btn>
</template>

<script>
import {post_text_request} from "@/requests"
import {post_voice_request} from "@/requests"

export default {
  data() {
    return {
      text_visible: true,
      send_text_visible: true,
      open_voice_visible: false,
      send_voice_visible: false,
      delete_voice_visible: false,
      player_visible: false,
      stop_voice_visible: false,
      audioSrc: null,
      audioBlob: null,
      mediaRecorder: null,
      chunks: [],
      isRunning: false,
      time: 0,
      timer: null,
      messages: [
        { content: 'Привет, чем могу помочь?', me: false, created_at: this.get_date() },
      ],
      newMessage: ''
    }
  },

  created() {

    if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
      navigator.mediaDevices.getUserMedia({ audio: true })
          .then(stream => {
            // Доступ к микрофону разрешен
            this.open_voice_visible = true;
          })
          .catch(error => {
            console.log('Ошибка доступа к микрофону:', error);
          });
    } else {
      console.log('getUserMedia не поддерживается в этом браузере');
    }
  },

  computed: {
    formatTime() {
      const minutes = Math.floor(this.time / 60);
      const seconds = (this.time % 60).toFixed(1); // Форматируем с точностью до одного знака после запятой
      return `${minutes}:${seconds < 10 ? '0' : ''}${seconds}`;
    }
  },

  mounted() {
    document.addEventListener('keydown', this.handleKeyPress);
  },
  beforeDestroy() {
    document.removeEventListener('keydown', this.handleKeyPress);
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
        post_text_request(this.$store.getters.getState.course,
            this.$store.getters.getState.subject, this.newMessage, (res) => this.create_message(res, false));
        this.newMessage = '';
      }
    },

    restart() {
      this.$router.push('/');
    },

    start_voice() {
      this.startTimer()
      this.open_voice()
      this.audioSrc = null

      navigator.mediaDevices.getUserMedia({ audio: true })
          .then(stream => {
            this.mediaRecorder = new MediaRecorder(stream);
            this.mediaRecorder.ondataavailable = event => {
              this.chunks.push(event.data);
            };
            this.mediaRecorder.onstop = async () => {
                const blob = await new Blob(this.chunks, {type: 'audio/mpeg'});
                this.audioBlob = await blob;
                this.audioSrc = URL.createObjectURL(blob);
                await this.mediaRecorder.stream.getTracks().forEach(track => track.stop());
                this.mediaRecorder = null;
                this.chunks = [];
            };
            this.mediaRecorder.start();
          })
          .catch(error => {
            console.error('Error accessing microphone:', error);
          });
    },

    open_voice(){
      this.text_visible = false
      this.send_text_visible = false
      this.open_voice_visible = false
      this.send_voice_visible = true
      this.delete_voice_visible = true
      this.stop_voice_visible = true
      this.isRunning = true
    },

    close_voice() {
      this.text_visible = true
      this.send_text_visible = true
      this.open_voice_visible = true
      this.send_voice_visible = false
      this.delete_voice_visible = false
      this.player_visible = false
      this.stop_voice_visible = false
      this.stopTimer()
    },

    async send_voice() {
      await this.stop_voice()
      this.close_voice()
      
      if(this.time > 12) {
        this.create_message(`Ваше аудиосообщение слишком долгое! Пожалуйста, запишите вопрос покороче. Максимальная длительность: 12 сек. У вас - ${this.time} сек.`, false)
        return;
      }
      this.create_message("Голосовое отправлено", true)
      setTimeout(() => post_voice_request(this.$store.getters.getState.course,
          this.$store.getters.getState.subject,
          this.audioBlob,
          (res) => this.create_message(res, false)), 100)
    },

    handleKeyPress(event) {
      if (this.send_voice_visible && event.key === 'Enter') {
          this.send_voice();
      }
      else if (this.delete_voice_visible && event.key === 'Escape') {
        this.delete_voice();
      }
    },

    stop_voice(){
      this.stop_voice_visible = false
      if(this.mediaRecorder) this.mediaRecorder.stop();
      this.isRunning = false
      this.player_visible = true
      this.stopTimer()
    },

    delete_voice() {
      this.close_voice()
      if(this.mediaRecorder) this.mediaRecorder.stop();
    },

    startTimer() {
      this.isRunning = true;
      this.time = 0
      this.timer = setInterval(() => {
        this.time += 0.1;
      }, 100);
    },

    stopTimer() {
      this.isRunning = false;
      clearInterval(this.timer);
    },
  }
}
</script>

<style scoped>
  #indicator{
    margin: 10px;
    animation:blinkingOpacity 1s infinite alternate;
  }

  #chat {
    position: relative;
    background: none;
    width: 50%;
    height: 93vh;
  }
  #messages {
    height: 80%;
    overflow-y: auto;
    display: flex;
    flex-direction: column-reverse;
  }

  #restart-button {
    position: fixed;
    margin: 10px;
    top: 0;
    right: 0;
    background-color: transparent;
  }

  @keyframes blinkingOpacity {
    from {
      opacity: 1;
    }
    to {
      opacity: 0.4;
    }
  }

</style>