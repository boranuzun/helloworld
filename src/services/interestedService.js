import api from "@/services/api"
import { ref } from "vue"

let interestingEvent = ref({})
let interestedInEvent = ref({})


export default {
    interestingEvent,

    interestedInEvent,

    // GET /interested
    getInterestingEvent(userId) {
        let apiString = `interested/`
        return api
            .get(apiString, { params: { user: userId } })
            .then((response) => {
                interestingEvent.value = response.data
            })
            .catch((error) => {
                console.error(error);
            });
    },

    // GET /interested/{id}
    getInterestedInEvent(eventId) {
        let apiString = `interested/`
        return api
            .get(apiString, { params: { event: eventId } })
            .then((response) => {
                interestedInEvent.value = response.data
            })
            .catch((error) => {
                console.error(error);
            });
    },

    // POST /interested
    postInterested(payload) {
        return api.post(`interested/`, payload).then((response) => response.data)
    },

    // DELETE /interested/{id}
    deleteInterested(interestedId) {
        return api.delete(`interested/${interestedId}`).then((response) => response.data)
    }
}