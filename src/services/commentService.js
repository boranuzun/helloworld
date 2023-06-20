import api from "@/services/api"
import { ref } from "vue"

let comments = ref({})

export default {
    comments,

    // GET /comments/?event={event}
    fetchCommentsByEvent(event) {
        let apiString = `comments/`
        return api
            .get(apiString, { params: { event: event } })
            .then((response) => {
                comments.value = response.data
            })
            .catch((error) => {
                console.error(error);
            });
    },

    // POST /comments
    postComment(payload) {
        return api.post(`comments/`, payload).then((response) => response.data)
    },

    emptyData() {
        this.comments.value = null
    }
}
