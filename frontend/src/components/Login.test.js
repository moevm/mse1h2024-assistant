// import { screen, fireEvent } from '@testing-library/vue'
// import Login from '@/components/Login.vue'
// import '@testing-library/jest-dom'
// import customRender from "@/customRender";
//
// // Мокируем get_courses из "@/requests"
// jest.mock('@/requests', () => ({
//     get_courses: jest.fn().mockResolvedValue({
//         course1: ['subject1', 'subject2'],
//         course2: ['subject3', 'subject4']
//     })
// }))
//
// describe('Login.vue', () => {
//     it('renders', () => {
//         const { debug } = customRender(Login)
//         debug()
//     })
//
//     it('отображает поля выбора курса и раздела', async () => {
//         // Рендерим компонент
//         customRender(Login)
//
//         const course = await screen.getByLabelText('Выберите номер курса')
//         const subject = await screen.getByLabelText('Выберите раздел')
//
//         // Проверяем, что поля выбора курса и раздела отображаются
//         expect(course).toBeInTheDocument()
//         expect(subject).toBeInTheDocument()
//     })
//
//     it('отображает кнопку "Начать" и проверяет ее доступность', async () => {
//         customRender(Login)
//         const startButton = await screen.getByText('Начать')
//         expect(startButton).toBeInTheDocument()
//     })
//
//     it('выбирает курс и проверят недоступность "Начать"', async () => {
//         // Рендерим компонент
//         customRender(Login)
//
//         const course = await screen.getByLabelText('Выберите номер курса')
//         const startButton = await screen.getByText('Начать')
//
//         await fireEvent.select(course, 'course1')
//
//         expect(startButton).toBeDisabled()
//     })
//
//     it('выбирает курс, предмет и проверят доступность "Начать" и корректность предмета', async () => {
//         customRender(Login)
//
//         const course = await screen.getByLabelText('Выберите номер курса')
//         const subject = await screen.getByLabelText('Выберите раздел')
//         const startButton = await screen.getByText('Начать')
//
//         await fireEvent.change(course, { target: { value: 'course1' } });
//         await fireEvent.change(subject, { target: { value: 'subject1' } });
//
//         expect(course.value).toBe('course1')
//
//         expect(startButton).not.toBeDisabled()
//     })
//
//     it('запускает сессию при нажатии на кнопку "Начать"', async () => {
//         // Рендерим компонент
//         customRender(Login)
//
//         // Ждем, пока выполняется запрос get_courses
//         await screen.findByText('Выберите номер курса')
//
//         // Выбираем курс и раздел
//         await fireEvent.select(screen.getByLabelText('Выберите номер курса'), 'course1')
//         await fireEvent.select(screen.getByLabelText('Выберите раздел'), 'subject1')
//
//         // Нажимаем на кнопку "Начать"
//         await fireEvent.click(screen.getByText('Начать'))
//
//         // Проверяем, что вызваны соответствующие мутации Vuex и переход на страницу чата
//         expect(mockRouter.push).toHaveBeenCalledWith('/chat')
//         expect(mockStore.commit).toHaveBeenCalledWith('setCourse', 'course1 курс')
//         expect(mockStore.commit).toHaveBeenCalledWith('setSubject', 'subject1')
//     })
// })
