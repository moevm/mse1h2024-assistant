import {instance} from "@/main";

export async function post_text_request(course, subject, text){
    console.log({course: course,
        subject: subject,
        text: text})
    let response = await instance.post("/api/send_text_request", {course: course,
      subject: subject,
      text: text})

    return response.data.is_ok
}

export async function post_voice_request(course, subject, formData){
    let response = await instance.post('your_server_url',
        {
            data: formData,
            subject: subject,
            text: text
        },
        {
            headers: {
                'Content-Type': 'multipart/form-data'
        }
    })

    return response.data.is_ok
}