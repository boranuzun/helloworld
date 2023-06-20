import { createApp } from "vue"
import App from "./App.vue"
import router from "./router"

/***********  https://fontawesome.com/ ************/

/* import the fontawesome core */
import { library } from "@fortawesome/fontawesome-svg-core"

/* import font awesome icon component */
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome"

/* import individual icons */
import {
  faTwitter,
  faReddit,
  faTwitterSquare,
  faInstagramSquare,
  faGithubSquare,
  faWhatsapp
} from "@fortawesome/free-brands-svg-icons"
import { faHeart, faSquarePlus, faArrowLeft } from "@fortawesome/free-solid-svg-icons"
import { faHeart as farHeart, faComment, faUser } from "@fortawesome/free-regular-svg-icons"

/* add icons to the library */
library.add(
  faTwitter,
  faReddit,
  faTwitterSquare,
  faInstagramSquare,
  faGithubSquare,
  faHeart,
  farHeart,
  faWhatsapp,
  faSquarePlus,
  faComment,
  faArrowLeft,
  faUser
)

const app = createApp(App)
app.use(router)
app.component("font-awesome-icon", FontAwesomeIcon)
app.mount("#app")
