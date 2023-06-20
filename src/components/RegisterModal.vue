<!-- Based on https://vuejsexamples.com/build-a-custom-modal-component-in-vue-js/ -->

<template>
  <div class="modal-overlay-register" @click="$emit('close-modal')">
    <div class="modal-register" @click.stop>
      <div id="designTop">
        <h4>Account creation</h4>
        <p>With an account you can like your favorite events and even post your own!</p>
        <img v-bind:src="userData.profilePic" />
        <br />
      </div>
      <div id="designBottom">
        <button id="changeImage" @click="randomizeImage">Change image</button>
        <p>Username</p>
        <input type="text" class="form-control" placeholder="Username" v-model="userData.username" />
        <p>Email</p>
        <input type="text" class="form-control" placeholder="jane.doe@example.com" v-model="userData.email" />
        <p>Password1</p>
        <input type="password" class="form-control" placeholder="qwertz" v-model="userData.password1" />
        <p>Password2</p>
        <input type="password" class="form-control" placeholder="qwertz" v-model="userData.password2" />
        <br />

        <button id="cancel" @click="$emit('close-modal')">Cancel</button>
        <button id="create" @click="registerNewUser">Create user</button>
      </div>
    </div>

    <div class="close" @click="$emit('close-modal')"></div>
  </div>
</template>

<script>
export default {
  data() {
    //
    return {
      userData: {
        username: "",
        email: "",
        password1: "",
        password2: "",
        is_staff: false,
        is_active: true,
        profilePic: "https://api.multiavatar.com/xxxx.svg"
      }

    }
  },

  methods: {
    // POST new user via Header.vue's registerNewUser that then calls src\services\userService.js
    registerNewUser() {
      this.$parent.registerNewUser(
        this.userData
      )
    },

    randomizeImage() {
      let apiImage = "https://api.multiavatar.com/"
      let random = (Math.random() + 1).toString(36).substring(7)
      let apiImageEnd = ".svg"
      this.userData.profilePic = apiImage + random + apiImageEnd
    }
  }
}
</script>

<style scoped>
.modal-overlay-register {
  display: block;
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  z-index: 9999;
}

.modal-register {

  position: absolute;

  top: 45%;
  left: 50%;
  transform: translate(-50%, -50%);
  background-color: #fff;

  text-align: center;
  background-color: white;
  width: fit-content;
  margin: 30px;
  border-radius: 20px;
  height: fit-content;
  max-height: 95%;
  overflow-y: auto;
}

@media only screen and (max-width: 992px) {
  .modal-register {

    position: absolute;

    top: 45%;
    left: 50%;
    transform: translate(-50%, -50%);
    background-color: #fff;

    text-align: center;
    background-color: white;

    margin: 30px;
    margin-left: 0px;
    border-radius: 20px;
    height: fit-content;
    max-height: 95%;

    min-width: 430px;
  }
}

@media only screen and (max-width: 430px) {
  .modal-register {

    position: absolute;

    top: 45%;
    left: 50%;
    transform: translate(-50%, -50%);
    background-color: #fff;

    text-align: center;
    background-color: white;

    margin: 30px;
    margin-left: 0px;
    border-radius: 20px;
    height: fit-content;
    max-height: 95%;

    min-width: 100%;
  }
}

.close {
  margin: 10% 0 0 16px;
  cursor: pointer;
}

.close-img {
  width: 25px;
}

.check {
  width: 150px;
}

h4 {
  font-weight: 500;
  font-size: 28px;
  margin: 0px 0;
}

p {
  font-size: 16px;
  margin-bottom: 6px;
}

button {
  background-color: #717053;
  width: 150px;
  height: 40px;
  color: white;
  font-size: 14px;
  border-radius: 12px;
  margin: 4px;
  margin-top: 8px;
  border: none;
  font-weight: bold;
  cursor: pointer;
}

#changeImage {
  margin-bottom: 2em;
  background-color: blue;
}

#create {
  background-color: blue;
  margin-top: 16px;
}

#cancel {
  background-color: red;
  margin-top: 16px;
}

img {
  justify-self: center;
  width: 16vh;
  height: auto;
}

button:hover {
  background-color: black;
  transition: 0.7s;
}

button:active {
  transform: translateY(2px);
}

#designTop {
  background-color: grey;
  color: white;
  padding: 20px;
  padding-bottom: 8px;
  margin-bottom: 8px;
  border-top-right-radius: 20px;
  border-top-left-radius: 20px;
}

#designBottom {
  margin-left: 10%;
  margin-right: 10%;
}

#designTop * {
  margin-top: 4px;
  margin-bottom: 4px;
}
</style>
