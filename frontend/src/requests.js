import {instance} from "@/main";

export async function post_text_request(course, subject, text, callback){
    console.log("SEND: " + {course: course,
        subject: subject,
        text: text})
    let response = await instance.post("/api/ask_model_by_text_request", {course: course,
      subject: subject,
       text: text})
    const interval = setInterval(() => {
        get_task_result(response.data.text)
        .then(res => {
            if(res.data.task_status == 'SUCCESS') {
                clearInterval(interval);
                callback(res.data.task_result);
            }
            console.log("res: ", res);
        })
    }, 5000);
}

export async function get_task_result(task_id) {
    return await instance.get("/api/tasks/" + task_id);
}

export async function post_voice_request(course, subject, formData, callback){
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
    const interval = setInterval(() => {
        get_task_result(response.data.text)
        .then(res => {
            if(res.data.task_status == 'SUCCESS') {
                clearInterval(interval);
                callback(res.data.task_result);
            }
            console.log("res: ", res);
        })
    }, 5000);
}

export async function get_courses(){
    let response =  await instance.get('/api/get_courses')
    return response.data
}