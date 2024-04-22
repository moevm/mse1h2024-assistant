module.exports = {
    testEnvironment: 'jsdom',
    moduleFileExtensions: ['js', 'json', 'vue'],
    transform: {
        '^.+\\.js$': 'babel-jest',
        '^.+\\.vue$': '@vue/vue3-jest'
    },
    setupFilesAfterEnv: ['./tests/unit/setup.js'],
    testEnvironmentOptions: {
        customExportConditions: ["node", "node-addons"],
    },
}