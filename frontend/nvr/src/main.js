import { createApp } from 'vue'
import App from './App.vue'
import "bootstrap/dist/css/bootstrap.min.css";
import "@/assets/css/main.css";

var app = createApp(App)
app.mount('#app')
app.config.globalProperties["$BASE_URL"] = "http://localhost:5000";
