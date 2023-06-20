<!-- Source  https://getbootstrap.com/docs/5.2/examples/headers/  & https://getbootstrap.com/docs/5.2/components/dropdowns/-->
<template>
  <header class="bg-light">
    <div class="container">
      <!-- Logo -->
      <a href="#" class="d-flex align-items-center mb-2 mb-lg-0 text-dark text-decoration-none">
        <img src="../assets/hello-world-white.png" width="100" height="100" alt="Hello World Logo" />
      </a>

      <!-- Hello World text -->
      <div class="d-flex flex-wrap align-items-center justify-content-center justify-content-lg-center" id="fontTest">
        <a href="#">
          <h1>Hello World!</h1>
        </a>
      </div>

      <!-- User picture and dropdown menu -->
      <div class="dropdown text-end" v-if="user">
        <a href="#" class="d-block link-dark text-decoration-none dropdown-toggle" data-bs-toggle="dropdown"
          aria-expanded="false">
          <img id="pp" v-bind:src="this.customUser.profilePic" alt="mdo" class="rounded-circle" />
        </a>
        <ul class="dropdown-menu text-small">
          <li>
            <h6 class="dropdown-header">Profile</h6>
          </li>
          <li>
            <a class="dropdown-item" href="#/ProfileView">
              <b>{{ this.user.username }} </b></a>
          </li>
          <li><br /></li>
          <li>
            <h6 class="dropdown-header">Create</h6>
          </li>
          <li><a class="dropdown-item" href="#/CreateEventView">New event...</a></li>
          <li><a class="dropdown-item" href="#/CreatePlaceView">New place...</a></li>
          <li>
            <hr class="dropdown-divider" />
          </li>
          <li><a class="dropdown-item" @click="logout" href="#">Sign out</a></li>
        </ul>
      </div>
      <div class="dropdown text-end" v-else>
        <a href="#" id="loginPrompt" class="d-block link-dark text-decoration-none dropdown-toggle"
          data-bs-toggle="dropdown" aria-expanded="false">
          <img id="pp" src="../assets/defaultUser.png" alt="mdo" class="rounded-circle" />
        </a>
        <div class="dropdown-menu" id="loginPromptDropDown">
          <form class="px-4 py-3" @submit.prevent="login">
            <div class="mb-3">
              <label for="username" class="form-label">Username</label>
              <input type="text" class="form-control" v-model="username" @keyup.enter="login" id="username"
                placeholder="Username" />
            </div>
            <div class="mb-3">
              <label for="password" class="form-label">Password</label>
              <input type="password" class="form-control" v-model="password" @keyup.enter="login" id="password"
                placeholder="Password" />
            </div>
            <div class="mb-3"></div>
            <button type="submit" class="btn btn-primary">Sign in</button>
          </form>
          <div class="dropdown-divider"></div>
          <a class="dropdown-item" href="#" @click="showModal = true">New around here? Sign up</a>
        </div>
      </div>
    </div>
  </header>

  <registerModal v-show="showModal" @close-modal="showModal = false" />
</template>

<script>
import authService from "../services/authService"
import userService from "../services/userService"
import registerModal from "./RegisterModal.vue"

export default {
  name: "HeaderVue",
  components: { registerModal },
  data() {
    return {
      showModal: false,
      showLoginModal: false
    }
  },

  async mounted() {
    await authService.getUser()
  },

  computed: {
    user() {
      return authService.user.value
    },

    customUser() {
      return userService.customUser.value
    }
  },

  watch: {
    "authService.user.value"(newValue) {
      this.isLoggedIn = !!newValue
    }
  },

  methods: {
    async login() {
      this.loginError = ""

      try {
        await authService.login({
          username: this.username,
          password: this.password
        })

        // Refresh the page
        // https://www.freecodecamp.org/news/javascript-refresh-page-how-to-reload-a-page-in-js/#:~:text=The%20simplest%20way%20to%20refresh,and%20loading%20the%20latest%20content.
        window.location.reload()
      } catch (err) {
        this.loginError = err.response.data
        alert(err.response.data.non_field_errors[0]) // A afficher dans une modal ?
      }
    },

    logout() {
      authService.logout()
    },

    registerNewUser(payload) {
      authService.register(payload)
      this.showModal = false
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
a {
  color: inherit;
  text-decoration: none;
}

#nav {
  background-color: #ccc;
}

#head {
  display: flex;
  align-items: center;
  background-color: #aaa;
}

#begin {
  min-width: 33%;
}

#begin * {
  display: flex;
  justify-content: left;
}

#mid {
  min-width: 33%;
}

#mid * {
  display: flex;
  justify-content: center;
}

#end {
  min-width: 33%;
}

#end * {
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
  justify-content: right;
  align-items: center;
}

#pp {
  width: 3.5em;
  height: auto;
}

#header {
  position: sticky;
  top: 0;
  z-index: 999;
}

.text-end {
  margin-right: 20px;
}

#fontTest * {
  display: flex;
  font-family: "Chewy";
  font-size: 56px;
  color: whitesmoke;
}

.container {
  min-width: 100%;
  margin-bottom: 1em !important;
  display: flex;
  align-items: center;
  justify-items: space-between;
  justify-content: space-between;
}

header {
  background: #90a6bd;
  /* fallback for old browsers */
  background: -webkit-linear-gradient(to left, #90a6bd, #4ecdc4);
  /* Chrome 10-25, Safari 5.1-6 */
  background: linear-gradient(to left, #90a6bd, #4ecdc4);
  /* W3C, IE 10+/ Edge, Firefox 16+, Chrome 26+, Opera 12+, Safari 7+ */

  background: #8360c3;
  /* fallback for old browsers */
  background: -webkit-linear-gradient(to right, #2ebf91, #8360c3);
  /* Chrome 10-25, Safari 5.1-6 */
  background: linear-gradient(to right, #2ebf91, #8360c3);
  /* W3C, IE 10+/ Edge, Firefox 16+, Chrome 26+, Opera 12+, Safari 7+ */

  background: #c2e59c;
  /* fallback for old browsers */
  background: -webkit-linear-gradient(to right, #64b3f4, #c2e59c);
  /* Chrome 10-25, Safari 5.1-6 */
  background: linear-gradient(to right, #64b3f4, #c2e59c);
  /* W3C, IE 10+/ Edge, Firefox 16+, Chrome 26+, Opera 12+, Safari 7+ */
}
</style>
