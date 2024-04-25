import { screen } from '@testing-library/vue';
import Chat from '@/components/Chat.vue';
import customRender from "@/customRender";
import '@testing-library/jest-dom'



describe('Chat', () => {
    it('должен отображать начальное состояние компонента', () => {
        customRender(Chat);

        expect(screen.getByTestId('text-test')).toBeInTheDocument();
        expect(screen.getByTestId('send-test')).toBeInTheDocument();
        expect(screen.getByTestId('voice-test')).toBeInTheDocument();
    });
});