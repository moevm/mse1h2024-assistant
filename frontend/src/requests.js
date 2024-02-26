import {instance} from "@/main";

export async function post_request(course, subject, text){
    console.log({course: course,
        subject: subject,
        text: text})
    let response = await instance.post("/api/send_text_request", {course: course,
      subject: subject,
      text: text})

    return response.data.is_ok
}