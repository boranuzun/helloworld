import api from "@/services/api"
import { ref } from "vue"

let events = ref([])

export default {
  events,

  // POST /events
  postEvent(payload) {
    return api.post(`events/`, payload).then((response) => response.data)
  },

  // GET /events
  fetchEvents() {
    return api.get(`events/`).then((response) => events.value = response.data)
  },

  // GET /events/{id}
  fetchEventById(id) {
    return api.get(`events/${id}`).then((response) => response.data)
  },

  // DELETE /events/{id}
  deleteEvent(id) {
    return api.delete(`events/${id}`).then((response) => response.data)
  }
}