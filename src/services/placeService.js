import api from "@/services/api"
import { ref } from "vue"

let places = ref([])

export default {
  places,

  // POST /places
  postPlace(payload) {
    return api.post(`places/`, payload).then((response) => response.data)
  },

  // GET /places
  fetchPlaces() {
    return api.get(`places/`).then((response) => places.value = response.data)
  },

  // GET /places/{id}
  fetchPlaceById(id) {
    return api.get(`places/${id}`).then((response) => response.data)
  },

  // PUT /places/{id}
  deletePlace(id) {
    return api.delete(`places/${id}`).then((response) => response.data)
  }
}