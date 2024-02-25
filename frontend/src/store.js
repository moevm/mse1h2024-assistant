import { createStore } from 'vuex';

const store = createStore({
    state() {
        let data  = JSON.parse(localStorage.getItem("store_data"))
        return {
            Data: data !== null ? data : {}
        };
    },
    mutations: {
        setCourse(state, course) {
            state.Data.course = course;
            localStorage.setItem("store_data", JSON.stringify(state.Data))
        },
        setSubject(state, subject){
            state.Data.subject = subject;
            localStorage.setItem("store_data", JSON.stringify(state.Data))
        },
    },
    getters: {
        getState: state => state.Data
    }
});

export default store;