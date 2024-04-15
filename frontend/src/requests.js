import {instance} from "@/main";

export async function post_request(course, subject, text){
    console.log("SEND: " + {course: course,
        subject: subject,
        text: text})
    let response = await instance.post("/api/ask_model_by_text_request", {course: course,
      subject: subject,
      text: text})
      console.log("RESPONSE: " + response.data.text);
    return response.data.text;
}

export async function post_voice_request(course, subject, formData){
  formData.append("course", course)
  formData.append("subject", subject)
  let response = await instance.post('/api/send_voice_request',
      formData,
      {
          headers: {
              'Content-Type': 'multipart/form-data'
          }
      }
  )

  return response.data.text;
}