import {instance} from "@/main";

describe("API backend", () => {
    it('should get courses and subjects', async () => {
        const response = await instance.get('/api/get_courses');
        expect(response.status).toBe(200);
    });

    it('should post message', async () => {
        const response = await instance.post("/api/ask_model_by_text_request",
            {
                course: "course",
                subject: "subject",
                text: "text"
            });
        expect(response.status).toBe(200);
    });

    it('should send voice message', async () => {
        const formData = new FormData();
        formData.append("audio", new Blob([], {type: 'audio/mpeg'}));
        formData.append("course", "course");
        formData.append("subject", "subject");
        const response = await instance.post('/api/send_voice_request',
            formData,
            {
                headers: {
                    'Content-Type': 'multipart/form-data'
                }
            }
        )
        expect(response.status).toBe(200);
    });




})