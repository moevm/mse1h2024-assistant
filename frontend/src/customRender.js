import { render } from "@testing-library/vue";
import vuetify from "@/main";

export default function customRender(component, options) {
    return render(component, {
        ...options,
        global: {
            ...options?.global,
            plugins: [vuetify, ...(options?.global?.plugins || [])]
        }
    });
}