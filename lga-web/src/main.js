import { createApp } from 'vue'

import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import App from './App.vue'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'
import { createPinia } from 'pinia'
import axios from 'axios'
import VueAxios from 'vue-axios'

// import setupLocatorUI from "@locator/runtime";
//
// if (process.env.NODE_ENV === "development") {
//   setupLocatorUI({
//     adapter: "vue"
//   });
// }

const app = createApp(App)
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component)
}
app.use(ElementPlus)
app.use(createPinia())
app.use(VueAxios, {http: axios, axios: axios })
app.provide('axios', app.config.globalProperties.axios)
app.provide('http', app.config.globalProperties.http)
app.mount('#app')
