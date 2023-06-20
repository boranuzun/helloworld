import api from "@/services/api"
import { ref } from "vue"

import userService from '../services/userService';
import interestedService from "./interestedService";

// it would be better to store refresh token and then use it to get a new access token
const LOCALSTORARGE_TOKEN_KEY = "myapp_access_token"
let access_token = localStorage.getItem(LOCALSTORARGE_TOKEN_KEY)
let user = ref()

api.interceptors.request.use((config) => {
  if (access_token) {
    config.headers["Authorization"] = `Bearer ${access_token}`
  }
  return config
})

export default {
  user,

  login(payload) {
    if (!payload.username || !payload.password) {
      return Promise.reject("Username and password are required.")
    }

    return api.post(`dj-rest-auth/login/`, payload).then((response) => {
      access_token = response.data.access_token
      localStorage.setItem(LOCALSTORARGE_TOKEN_KEY, access_token)
      user.value = response.data.user
      userService.getCustomUser(user.value.pk)
      interestedService.getInterestingEvent(user.value.pk)
      return response.data.user
    })
  },

  logout() {
    return api.post(`dj-rest-auth/logout/`).then((response) => {
      access_token = undefined
      localStorage.removeItem(LOCALSTORARGE_TOKEN_KEY)
      user.value = undefined
      userService.customUser.value = undefined
      return response.data
    })
  },

  register(payload) {
    return api.post(`register/`, payload).then((response) => {
      access_token = response.data.access_token
      user.value = response.data.user
      this.getUser();
      return response.data.user
    }).catch(
      function (error) {
        console.log('Show error notification!')
        alert(error.message + " " + JSON.stringify(error.response.data))
        return Promise.reject(error)
      }
    )
  },

  // allows to relogin with saved token
  getUser() {
    return api.get(`dj-rest-auth/user/`).then((response) => {
      user.value = response.data
      userService.getCustomUser(user.value.pk) // ????
      //Fetch list of event that the user that was just returned is interested in
      interestedService.getInterestingEvent(user.value.pk)
    })
  },
}
