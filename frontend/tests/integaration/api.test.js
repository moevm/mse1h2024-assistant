import {instance} from "@/main";
import {get_courses} from "@/requests";

describe("API backend", () => {
    it('should get courses and subjects', async () => {
        const response = await get_courses;
        expect(response.status).toBe(200);
    });
})