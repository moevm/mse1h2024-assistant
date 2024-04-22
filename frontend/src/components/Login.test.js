import { screen, fireEvent } from '@testing-library/vue'
import Login from '@/components/Login.vue'
import '@testing-library/jest-dom'
import customRender from "@/customRender";

// Мокируем get_courses из "@/requests"
jest.mock('@/requests', () => ({
    get_courses: jest.fn().mockResolvedValue({
        course1: ['subject1', 'subject2'],
        course2: ['subject3', 'subject4']
    }),
    data:() => {
        return {
            course: '',
            subject: '',
            courses: [],
            subjects: [],
            back_data: {}
        }
    },
}))

describe('Login.vue', () => {
    it('renders', () => {
        const { debug } = customRender(Login)
        debug()
    })

    it('отображает поля выбора курса и раздела', async () => {
        customRender(Login)

        const course = await screen.getByLabelText('Выберите номер курса')
        const subject = await screen.getByLabelText('Выберите раздел')

        expect(course).toBeInTheDocument()
        expect(subject).toBeInTheDocument()
    })

    it('проверяет на пустоту курс и предмет', async () => {
        customRender(Login)

        const course = await screen.getByLabelText('Выберите номер курса')
        const subject = await screen.getByLabelText('Выберите раздел')

        expect(course.value).toBe('')
        expect(subject.value).toBe('')
    })

    it('отображает кнопку "Начать" и проверяет ее недоступность и недоступность выбора предмета', async () => {
        customRender(Login)
        const startButton = await screen.getByTestId('start-test')
        const subject = await screen.getByLabelText('Выберите раздел')

        expect(startButton).toBeInTheDocument()
        expect(startButton).toBeDisabled()
        expect(subject).toBeDisabled()
    })

    it('выбирает курс и проверят недоступность "Начать"', async () => {
        customRender(Login)

        const course = await screen.getByLabelText('Выберите номер курса')
        const startButton = await screen.getByTestId('start-test')

        await fireEvent.change(course, { target: { value: 'course1' } });

        expect(startButton).toBeDisabled()
    })
})
