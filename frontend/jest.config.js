module.exports = {
    testEnvironment: 'jsdom',
    testEnvironmentOptions: {
        customExportConditions: ["node", "node-addons"],
    },
    moduleFileExtensions: ['js', 'json', 'vue', 'sass', 'css', 'mjs'],
    transform: {
        '^.+\\.js$': 'babel-jest',
        '^.+\\.vue$': '@vue/vue3-jest',
        "^.+\\.mjs$": "babel-jest",
    },
    setupFilesAfterEnv: ['./tests/unit/setup.js'],
    moduleNameMapper: {
        ".+\\.(css|styl|less|sass|scss|png|jpg|svg|ttf|woff|woff2)$":"<rootDir>/tests/unit/styleMock.js",
        "^vuetify/components$": "<rootDir>/node_modules/vuetify/lib/components/index.mjs",
        "^vuetify/directives$": "<rootDir>/node_modules/vuetify/lib/directives/index.mjs",
    },
    transformIgnorePatterns: ['/node_modules/(?!(vuetify)/)'],
};