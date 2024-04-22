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
//                 'Курс 1': ['Раздел 1', 'Раздел 2'],
//                 'Курс 2': ['Раздел 3', 'Раздел 4']
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