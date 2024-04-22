// // import { render } from '@testing-library/vue'
// // import Login from './Login.vue'
// //
//
//
// import { render, fireEvent} from '@testing-library/vue'
// import Login from './Login.vue'
// import '@testing-library/jest-dom'
//
// test('1) render', () => {
//     const { debug } = render(Login)
//
//     debug()
// })
//
// test('2) renders base button', () => {
//     const { getByText } = render(Login)
//     const button = getByText('Начать')
//     console.log(button)
//     expect(button).toBeInTheDocument()
// })
//
// test('3) course selection enables subject selection', async () => {
//     const { getByLabelText, getByText } = render(Login, {
//         data: () => ({
//             back_data: {
//                 courses: ['Курс 1', 'Курс 2'],
//                 subjects: {
//                     'Курс 1': ['Раздел 1', 'Раздел 2'],
//                     'Курс 2': ['Раздел 3', 'Раздел 4']
//                 }
//             }
//         })
//     })
//
//     const courseSelect = getByText('Выберите номер курса')
//     const subjectSelect = getByText('Выберите раздел')
//
//     // Изначально выбор раздела должен быть заблокирован
//     expect(subjectSelect).toBeDisabled()
//
//     // Выбираем курс
//     await fireEvent.update(courseSelect, 'Курс 1')
//
//     // Теперь выбор раздела должен быть доступен
//     expect(subjectSelect).not.toBeDisabled()
// })
//
// test('4) start button is disabled when course or subject is not selected', () => {
//     const { getByText } = render(Login)
//     const button = getByText('Начать')
//     expect(button).toBeDisabled()
// })
//
// test('5) start button navigates to chat page when course and subject are selected', async () => {
//     const { getByLabelText, getByText, emitted } = render(Login, {
//         data: () => ({
//             back_data: {
//                 'Курс 1': ['Раздел 1', 'Раздел 2']
//             }
//         }),
//         global: {
//             mocks: {
//                 $router: {
//                     push: jest.fn()
//                 },
//                 $store: {
//                     commit: jest.fn(),
//                     getters: {
//                         getState: () => ({ course: 'Курс 1', subject: 'Раздел 1' })
//                     }
//                 }
//             }
//         }
//     })
//
//     const courseSelect = getByLabelText('Выберите номер курса')
//     const subjectSelect = getByLabelText('Выберите раздел')
//     const button = getByText('Начать')
//
//     await fireEvent.update(courseSelect, 'Курс 1')
//     await fireEvent.update(subjectSelect, 'Раздел 1')
//     await fireEvent.click(button)
//
//     expect(emitted().click).toBeTruthy()
//     expect(window.$router.push).toHaveBeenCalledWith('/chat')
//     expect(window.$store.commit).toHaveBeenCalledWith('setCourse', 'Курс 1 курс')
//     expect(window.$store.commit).toHaveBeenCalledWith('setSubject', 'Раздел 1')
// })

import { render, screen, fireEvent } from '@testing-library/vue'
import Login from '@/components/Login.vue'
import '@testing-library/jest-dom'

// Мокируем get_courses из "@/requests"
jest.mock('@/requests', () => ({
    get_courses: jest.fn().mockResolvedValue({
        course1: ['subject1', 'subject2'],
        course2: ['subject3', 'subject4']
    })
}))

describe('Login.vue', () => {
    it('отображает поля выбора курса и раздела', async () => {
        // Рендерим компонент
        render(Login)

        const course = await screen.getByTestId('course-test')
        const subject = await screen.getByTestId('subject-test')

        // Проверяем, что поля выбора курса и раздела отображаются
        expect(course).toBeInTheDocument()
        expect(subject).toBeInTheDocument()
    })

    it('отображает кнопку "Начать" и проверяет ее доступность', async () => {
        render(Login)
        const startButton = await screen.getByTestId('start-test')
        expect(startButton).toBeInTheDocument()
    })

    // it('выбирает курс и проверят недоступность "Начать"', async () => {
    //     // Рендерим компонент
    //     render(Login)
    //
    //     const course = await screen.getByTestId('course-test')
    //
    //     const startButton = await screen.getByTestId('start-test')
    //
    //     await fireEvent.select(course, 'course1')
    //
    //     // Проверяем, что разделы появились и кнопка разблокировалась
    //     expect(await screen.getByTestId('subject-test')).toBeInTheDocument()
    //     expect(startButton).not.toBeDisabled()
    //
    //     // Выбираем раздел
    //     await fireEvent.select(screen.getByLabelText('Выберите раздел'), 'subject1')
    //
    //     // Проверяем, что кнопка остается разблокированной после выбора раздела
    //     expect(startButton).not.toBeDisabled()
    // })
    //
    // it('запускает сессию при нажатии на кнопку "Начать"', async () => {
    //     // Рендерим компонент
    //     render(Login)
    //
    //     // Ждем, пока выполняется запрос get_courses
    //     await screen.findByText('Выберите номер курса')
    //
    //     // Выбираем курс и раздел
    //     await fireEvent.select(screen.getByLabelText('Выберите номер курса'), 'course1')
    //     await fireEvent.select(screen.getByLabelText('Выберите раздел'), 'subject1')
    //
    //     // Нажимаем на кнопку "Начать"
    //     await fireEvent.click(screen.getByText('Начать'))
    //
    //     // Проверяем, что вызваны соответствующие мутации Vuex и переход на страницу чата
    //     expect(mockRouter.push).toHaveBeenCalledWith('/chat')
    //     expect(mockStore.commit).toHaveBeenCalledWith('setCourse', 'course1 курс')
    //     expect(mockStore.commit).toHaveBeenCalledWith('setSubject', 'subject1')
    // })
})
