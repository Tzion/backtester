// Import from ESM URLs (Deno style)
import { createApp } from "vue";
import App from "./App.vue";
import router from "./router.ts";

// Create and mount the Vue app
createApp(App)
  .use(router)
  .mount("#app");

console.log("Vue application initialized"); 