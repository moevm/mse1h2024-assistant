import { config } from '@vue/test-utils'

config.global.mocks = {
    $vuetify: {
        // Здесь вы можете добавить свойства и методы vuetify, необходимые в ваших тестах
    }
}