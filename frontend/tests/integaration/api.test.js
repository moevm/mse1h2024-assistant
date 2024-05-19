import {instance} from "@/main";

describe("API backend", () => {
    it('should get courses and subjects', async () => {
        const response = await instance.get('/api/get_courses');
        expect(response.status).toBe(200);
    });
})