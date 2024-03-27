import {instance} from "@/main";

export async function post_request(course, subject, text){
    console.log({course: course,
        subject: subject,
        text: text})
    let response = await instance.post("/api/ask_model_by_text_request", {course: course,
      subject: subject,
      text: text})

    console.log(response.data.text)
    return response.data.text
}