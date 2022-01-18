import { createApp } from 'vue'
import App from './App.vue'
import HelloWorld from './components/HelloWorld.vue'

// createApp(App).mount('#app')
const app = createApp(App)
const components = import.meta.globEager('./components/*.vue')
console.log(components);

Object.entries(components).forEach(([path, definition]) => {
    const componentName = path.split('/').pop()?.replace(/\.\w+$/, '')
    console.log(componentName)
    app.component(componentName as string, definition.default)
})

app.mount('#app')


