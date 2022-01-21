import { createApp } from 'vue'

import App from './App.vue'
import './index.css'

import Axios from 'axios'

import vueDebounce from 'vue-debounce'

import PrimeVue from 'primevue/config'
import Dialog from 'primevue/dialog'
import DataTable from 'primevue/datatable'
import Column from 'primevue/column';
import InputText from 'primevue/inputtext';

const app = createApp(App)
const components = import.meta.globEager('./components/*.vue')

Object.entries(components).forEach(([path, definition]) => {
    const componentName = path.split('/').pop()?.replace(/\.\w+$/, '')
    app.component(componentName as string, definition.default)
})

app.config.globalProperties.axios = Axios

app.use(vueDebounce, {
    listenTo: ['input', 'keyup'],
    defaultTime: '700ms',
})

app.use(PrimeVue)
// Prime Vue components
app.component('DataTable', DataTable)
app.component('Column', Column);
app.component('InputText', InputText);
app.component('Dialog', Dialog)

app.mount('#app')


