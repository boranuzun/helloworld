import api from "@/services/api"
import { ref } from "vue"

let customUser = ref()

export default {
  customUser,

  // GET /users/{id}
  getCustomUser(userId) {
    let apiString = `users/${userId}/`
    return api
      .get(apiString)
      .then((response) => {
        customUser.value = response.data
      })
      .catch((error) => {
        console.error(error)
      })
  },

  // GET /users
  fetchUsers() {
    return api.get(`users/`).then((response) => response.data)
  },

  // PUT /users/{id}
  patchUser(id, payload) {
    return api.patch(`users/${id}/`, payload).then((response) => response.data)
  }
}

