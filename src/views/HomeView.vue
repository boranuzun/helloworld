<template>
  <head>
    <title>HomeView</title>
  </head>

  <div>
    <!-- Search -->
    <br />
    <h1 style="font-family: 'caveat'; font-weight: bold">
      <span style="color: #2ebf91">Events</span> to <span style="color: #64b3f4">Reconnect</span>
    </h1>
    <div id="tuto">
      <p>
        Find events near you, meet people and make memories with
        <span style="font-family: Chewy">Hello World</span>
      </p>
      <button @click.stop="showLoginPrompt" class="unstyled-button">
        <p class="logwarn" v-if="!user">Log in to Like, Comment and Post!</p>
      </button>
    </div>

    <!-- Title filter -->
    <div class="filter-section">
      <div>
        <label>Try searching for a Karaoké or a bowling, whatever you like!</label>
        <input class="form-control" type="text" v-model="searchTitle" size="50" placeholder="Search by event name" />
      </div>

      <!-- Canton filter -->
      <div>
        <label>No locomotion? Check what's in your canton!</label>
        <input class="form-control" type="text" v-model="searchLocation" size="30" placeholder="Search by canton" />
      </div>

      <!-- Date filter -->
      <div>
        <label>What about tonight?</label>
        <input class="form-control" type="date" v-model="searchDate" />
      </div>

      <!-- Place filter -->
      <div>
        <label>A favorite park or pub?</label>
        <select class="form-control" id="place" v-model="selectedPlace" @change="filterEvents">
          <option value="">All Places</option>
          <option v-for="place in places" :key="place.id" :value="place.id">
            {{ place.venue_name }}
          </option>
        </select>
      </div>

      <!-- Reset filters -->
      <div>
        <label>Too picky?</label><br />
        <button @click="resetFilters" class="btn btn-secondary">Clear Filters</button>
      </div>
    </div>

    <div class="container">
      <hr />
    </div>
    <br />

    <!--Event cards-->
    <div v-if="filterEventsLength <= 0">
      <div class="container alert alert-danger" role="alert">
        No event matches your search criteria
      </div>
    </div>
    <div v-else class="container">
      <div class="row g-3">
        <div class="col-12 col-md-6 col-lg-4" v-for="event in paginatedEvents" :key="event.id">
          <div class="card" @click="showEventDetails(event)" style="cursor: context-menu">
            <div class="card-img-container">
              <img v-bind:src="event.event_pic" class="card-img-top" />
            </div>
            <div class="card-body">
              <h3 class="card-title">{{ event.title }}</h3>

              <ul class="list-group list-group-flush">
                <li class="list-group-item"></li>
                <li class="list-group-item">
                  {{ event.place.venue_name }}
                </li>
                <li class="list-group-item">
                  {{ event.place.address }}
                </li>
                <li class="list-group-item">{{ formatDate(event.date) }}</li>
              </ul>
              <div v-if="user">
                <div v-if="interestingEvents.includes(event.id)">
                  <button class="btn btn-white" @click.stop="deleteInterested(event.id)" style="margin-top: 10px">
                    <font-awesome-icon icon="fa-solid fa-heart" size="xl" style="color: #c84141" />
                  </button>
                </div>
                <div v-else>
                  <button class="btn btn-white" @click.stop="postInterested(event.id)" style="margin-top: 10px">
                    <font-awesome-icon :icon="['far', 'heart']" size="xl" style="color: #c84141" />
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <br />

      <!-- Page buttons -->
      <button v-for="page in totalPages" :key="page" @click="changePage(page)" id="page-button">
        {{ page }}
      </button>
    </div>
  </div>

  <!-- Modal component -->
  <transition name="modal">
    <div class="modal" v-if="showModal" @click="closeModal(false)">
      <div class="modal-content">
        <!-- Modal Header -->
        <div class="modal-header">
          <h3 class="modal-title">{{ selectedEvent.title }}</h3>
          <button class="close" @click="closeModal(true)">&times;</button>
        </div>
        <!-- Modal body -->
        <div class="modal-body">
          <!-- Event image -->
          <div id="modal-img">
            <img :src="selectedEvent.event_pic" class="modal-event-image" alt="Event Image" />
          </div>
          <!-- Display event details here -->
          <div class="modal-infos">
            <div v-if="!showComment && !showInterested">
              <div class="modal-description">
                <h3>Description</h3>
                <p>{{ selectedEvent.description }}</p>
              </div>
              <hr style="margin-left: 2em; margin-right: 2em; margin-bottom: 2em" />
              <div class="modal-address">
                <span class="modal-label">Date:</span>
                <span class="modal-value">{{ formatDate(selectedEvent.date) }}</span>
              </div>
              <div class="modal-address">
                <span class="modal-label">Place:</span>
                <span class="modal-value">
                  {{ selectedEvent.place.venue_name }}
                </span>
              </div>
              <div class="modal-address">
                <span class="modal-label">Address:</span>
                <span class="modal-value two-line-address">
                  {{ selectedEvent.place.address }},
                  {{ selectedEvent.place.zip }}
                  {{ selectedEvent.place.city }}
                </span>
              </div>
              <div>
                <span class="modal-label">Price:</span>
                <span class="modal-value">{{ selectedEvent.price }} CHF</span>
              </div>
              <div>
                <span class="modal-label">Capacity:</span>
                <span class="modal-value">{{ selectedEvent.event_capacity }}</span>
              </div>
              <div>
                <span class="modal-label">Creator:</span>
                <span class="modal-value"> {{ selectedEvent.creator.username }}</span>
              </div>
              <br />
              <hr style="margin-left: 2em; margin-right: 2em; margin-bottom: 2em" />
            </div>

            <!-- Buttons -->
            <div class="row">
              <div class="col-sm-12 text-center p-0">
                <button type="button" class="btn btn-labeled btn-outline-success" v-if="!showInterested" @click.stop="
                  this.showComment ? (this.showComment = false) : (this.showComment = true)
                  " style="margin: 5px; width: 15em">
                  <span class="btn-label" v-if="!showComment"><font-awesome-icon icon="fa-regular fa-comment" />
                    <span> Comments ({{ commentsLength }})</span>
                  </span>
                  <span class="btn-label" v-else><font-awesome-icon icon="fa-solid fa-arrow-left" />
                    <span> Hide Comments</span>
                  </span>
                </button>

                <button type="button" class="btn btn-laveled btn-outline-success" v-if="!showComment" @click.stop="
                  this.showInterested
                    ? (this.showInterested = false)
                    : (this.showInterested = true)
                  " style="margin: 5px; width: 15em">
                  <span class="btn-label" v-if="!showInterested"><font-awesome-icon icon="fa-regular fa-user" /><span>
                      Participants ({{ participantsLength }})</span></span>
                  <span class="btn-label" v-else><font-awesome-icon icon="fa-solid fa-arrow-left" />
                    <span> Hide Participants</span></span>
                </button>
              </div>
            </div>

            <br />

            <!-- Comments of the event-->
            <div v-if="this.comments != null && this.showComment" style="margin-left: 2em; margin-right: 2em">
              <div v-for="comment in paginatedComments" :key="comment.id">
                <!-- Boot strap -->
                <div class="card mb-3">
                  <div class="card-body">
                    <div class="d-flex flex-start">
                      <img class="rounded-circle shadow-1-strong me-3" :src="comment.user.profilePic" alt="avatar"
                        width="40" height="40" />
                      <div class="w-100">
                        <div class="d-flex justify-content-between align-items-center mb-3">
                          <h6 class="text-danger fw-bold mb-0 mt-2">
                            {{ comment.user.username }}
                          </h6>
                          <p class="mb-0" id="msgDate">{{ formatDate(comment.created_at) }}</p>
                        </div>
                        <div class="text-dark">{{ comment.msg }}</div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
              <!-- Post comment -->
              <div class="input-group mb-3" v-if="user">
                <input type="text" class="form-control" placeholder="Share your thoughts!"
                  aria-label="Share your thoughts!" aria-describedby="postComment" v-model="newComment"
                  @keyup.enter="postComment" />
                <button class="btn btn-outline-success" type="button" id="postComment" @click="postComment">
                  Send
                </button>
              </div>

              <div v-else>
                <a @click.stop="showLoginPrompt">
                  <div class="input-group mb-3">
                    <input type="text" class="form-control" placeholder="Log in to comment" aria-label="Log in to comment"
                      aria-describedby="postComment" disabled />
                    <button class="btn btn-outline-danger" type="button" @click="postComment" id="postComment" disabled>
                      Send
                    </button>
                  </div>
                </a>
              </div>
              <!-- Pagination buttons -->
              <div v-if="comments.length > commentsPerPage" style="text-align: center">
                <button v-for="pageNumber in Math.ceil(comments.length / commentsPerPage)" :key="pageNumber"
                  @click="commentPage = pageNumber" :class="{ active: pageNumber === commentPage }" id="page-button">
                  {{ pageNumber }}
                </button>
              </div>
            </div>

            <!-- User Interested in event -->
            <div v-if="this.showInterested">
              <div v-for="interested in interestedInEvent" :key="interested.id"
                style="display: flex; justify-content: center">
                <!-- Boot strap -->
                <div class="card mb-3" style="width: 18rem">
                  <div class="card-body">
                    <div class="d-flex">
                      <img class="rounded-circle shadow-1-strong me-3" :src="interested.user.profilePic" alt="avatar"
                        width="40" height="40" />
                      <h6 class="text-danger fw-bold position-absolute top-50 start-50 translate-middle">
                        {{ interested.user.username }}
                      </h6>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Modal footer -->
        <div class="modal-footer">
          <!-- Share button -->
          <a :href="getWhatsAppShareLink(selectedEvent)" target="_blank" rel="noopener noreferrer"
            class="btn btn-dark"><font-awesome-icon icon="fa-brands fa-whatsapp" beat-fade size="lg" />
            Share on Whatsapp
          </a>
          <a :href="getTwitterShareLink(selectedEvent)" target="_blank" rel="noopener noreferrer"
            class="btn btn-dark"><font-awesome-icon icon="fa-brands fa-twitter" beat-fade size="lg" />
            Share on Twitter
          </a>
          <a :href="getRedditShareLink(selectedEvent)" target="_blank" rel="noopener noreferrer"
            class="btn btn-dark"><font-awesome-icon icon="fa-brands fa-reddit" beat-fade size="lg" />
            Share on Reddit
          </a>
        </div>
      </div>
    </div>
  </transition>
</template>

<script>
import eventService from "../services/eventService"
import authService from "../services/authService"
import placeService from "../services/placeService"
import moment from "moment" // Import moment.js to format dates
import interestedService from "../services/interestedService"
import commentService from "../services/commentService"

export default {
  name: "HomeView",
  data() {
    return {
      // For filtering
      searchTitle: "",
      searchLocation: "",
      searchDate: "",
      selectedPlace: "",

      //For displaying events card
      currentPage: 1,
      itemsCommentsPerPage: 9,

      // Paylod to post new interested_in_event
      interestedData: {
        event: null,
        user: null
      },

      // For Modal of event details
      showModal: false,
      selectedEvent: null,
      showInterested: false,
      showComment: false,
      newComment: "",
      commentToPost: {
        user: null,
        event: null,
        msg: ""
      },
      commentPage: 1,
      commentsPerPage: 4
    }
  },
  async mounted() {
    // Fetch all events and places from the database
    await eventService.fetchEvents()
    await placeService.fetchPlaces()

    // After reload, to auto-scroll and go to correct page of last liked/unliked event
    if (localStorage.getItem("yCoordinate")) {
      this.currentPage = Number(localStorage.getItem("currentPage"))
      scroll(0, Number(localStorage.getItem("yCoordinate")))
      localStorage.removeItem("currentPage")
      localStorage.removeItem("yCoordinate")
    }

    // After reload, to show modal of event that was just commented
    if (localStorage.getItem("currentEvent")) {
      this.selectedEvent = localStorage.getItem("currentEvent")
      this.showEventDetails(JSON.parse(this.selectedEvent))
      this.showComment = true
      localStorage.removeItem("currentEvent")
    }
  },

  computed: {

    user() {
      return authService.user.value
    },

    events() {
      return [...eventService.events.value]
    },

    interestedInEvent() {
      return [...interestedService.interestedInEvent.value]
    },

    interestingEvents() {
      return [...interestedService.interestingEvent.value].map((e) => e.event)
    },

    places() {
      return placeService.places.value
    },

    filteredEvents() {
      return [...this.events].filter((event) => {
        const titleMatch =
          !this.searchTitle || event.title.toLowerCase().includes(this.searchTitle.toLowerCase())

        const locationMatch =
          !this.searchLocation ||
          event.place.state.toLowerCase().includes(this.searchLocation.toLowerCase())

        const dateMatch = !this.searchDate || moment(event.date).isSame(this.searchDate, "day")

        const placeMatch = !this.selectedPlace || event.place.id === this.selectedPlace

        return titleMatch && locationMatch && dateMatch && placeMatch
      })
    },

    // Function that returns the events that should be displayed on the current page
    paginatedEvents() {
      const startIndex = (this.currentPage - 1) * this.itemsCommentsPerPage
      const endIndex = startIndex + this.itemsCommentsPerPage
      const sortedEvents = this.sortEventsByDate(this.filteredEvents)
      return sortedEvents.slice(startIndex, endIndex)
    },

    // Function that returns the total number of pages
    totalPages() {
      return Math.ceil(this.filterEventsLength / this.itemsCommentsPerPage)
    },

    filterEventsLength() {
      return this.filteredEvents.length
    },

    // Modal
    // Function that returns the comments that should be displayed on the current page
    paginatedComments() {
      const startIndex = (this.commentPage - 1) * this.commentsPerPage
      const endIndex = startIndex + this.commentsPerPage
      return this.comments.slice(startIndex, endIndex)
    },

    participantsLength() {
      if (this.interestedInEvent === null) {
        return 0
      }
      return this.interestedInEvent.length
    },

    comments() {
      return [...commentService.comments.value].sort((a, b) => {
        // Convert the comment dates to Date objects for comparison
        const dateA = new Date(a.created_at)
        const dateB = new Date(b.created_at)

        // Sort the comments in descending order based on the date
        return dateB - dateA
      })
    },

    commentsLength() {
      if (this.comments === null) {
        return 0
      }
      return this.comments.length
    }
  },

  methods: {
    /************************* General *************************/
    showLoginPrompt() {
      this.closeModal(true)
      document.getElementById("loginPrompt").click()
    },

    // Method to sort events by date
    sortEventsByDate(events) {
      return events.slice().sort((a, b) => new Date(a.date) - new Date(b.date))
    },

    // Method that changes the current page
    changePage(page) {
      this.currentPage = page
    },

    // Method that formats the date using moment.js
    formatDate(date) {
      return moment(date).format("DD MMMM YYYY - HH:mm") // Customize the format as needed
    },

    // Method to reset the filters
    resetFilters() {
      this.searchTitle = ""
      this.searchLocation = ""
      this.searchDate = ""
      this.selectedPlace = ""
    },
    /************************* General *************************/

    /************************* Like/Dislike events *************************/
    async postInterested(eventId) {
      this.interestedData.event = eventId
      this.interestedData.user = authService.user.value.pk
      try {
        await interestedService.postInterested(this.interestedData)
        localStorage.setItem("yCoordinate", window.scrollY)
        localStorage.setItem("currentPage", this.currentPage)
        window.location.reload()
      } catch (err) {
        this.loginError = err.response.data
      }
    },

    async deleteInterested(eventId) {
      this.interestedData.event = eventId
      this.interestedData.user = authService.user.value.pk
      let toDelete = interestedService.interestingEvent.value.filter((e) => e.event == eventId)

      try {
        await interestedService.deleteInterested(toDelete[0].pk)

        // Refresh the page
        localStorage.setItem("yCoordinate", window.scrollY)
        localStorage.setItem("currentPage", this.currentPage)
        window.location.reload()
      } catch (err) {
        this.loginError = err.response.data
      }
    },
    /************************* Like/Dislike events *************************/

    /************************* Event modal *************************/
    // Method to show event details in a modal
    showEventDetails(event) {
      this.fetchCommentForEvent(event.id)
      this.selectedEvent = event
      this.showModal = true
    },

    // Method to close the modal when the user clicks outside of it
    closeModal(isModalCloseBtn) {
      // Check if the clicked element is the modal content or its child elements
      if (isModalCloseBtn) {
        this.showModal = false
        this.showComment = false
        this.showInterested = false
        commentService.emptyData()
      } else if (!event.target.closest(".modal-content")) {
        this.showComment = false
        this.showInterested = false
        this.showModal = false
        commentService.emptyData()
      }
    },
    /************************* Event modal *************************/

    /************************* Comments *************************/
    fetchCommentForEvent(event) {
      //Fetch all comments for the event that was clicked and stores them in commentService
      commentService.fetchCommentsByEvent(event)
      //Fetch all user interested by the event that was clicked and stores them in interestedService
      interestedService.getInterestedInEvent(event)
    },

    async postComment() {
      this.commentToPost.event = this.selectedEvent.id
      this.commentToPost.user = authService.user.value.pk
      this.commentToPost.msg = this.newComment
      try {
        await commentService.postComment(this.commentToPost)
        localStorage.setItem("currentEvent", JSON.stringify(this.selectedEvent))
        window.location.reload()
      } catch (err) {
        this.loginError = err.response.data
      }
    },
    /************************* Comments *************************/

    /************************* Share buttons *************************/
    // Method to get the WhatsApp share link for the selected event
    getWhatsAppShareLink(event) {
      const text = `Check out this event: ${event.title} on ${moment(event.date).format(
        "DD MMMM YYYY - HH:mm"
      )}`
      const url = encodeURIComponent(window.location.href)
      const whatsAppUrl = `https://api.whatsapp.com/send?text=${text} ${url}`
      return whatsAppUrl
    },

    // Method to get the Twitter share link for the selected event
    getTwitterShareLink(event) {
      const text = `Check out this event: ${event.title} on ${moment(event.date).format(
        "DD MMMM YYYY - HH:mm"
      )}`
      const url = encodeURIComponent(window.location.href)
      const hashtags = "event,HEG"
      const twitterUrl = `https://twitter.com/intent/tweet?text=${text}&url=${url}&hashtags=${hashtags}`
      return twitterUrl
    },

    // Method to get the Reddit share link for the selected event
    getRedditShareLink(event) {
      const title = encodeURIComponent(event.title)
      const url = encodeURIComponent(window.location.href)
      const redditUrl = `https://www.reddit.com/submit?title=${title}&url=${url}`
      return redditUrl
    },
    /************************* Share buttons *************************/

  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only. -->
<style scoped>
/* ------------------ Event cards --------------------- */
.card-img-top {
  object-fit: cover;
  height: 300px;
  transition: transform 0.5s ease;
}

.card-img-container {
  overflow: hidden;
  height: 300px;
}

.card-img-container:hover .card-img-top {
  transform: scale(1.1);
}

.card-body {
  height: auto;
}

.card:hover {
  box-shadow: 0 8px 16px 0 rgba(0, 0, 0, 0.2);
}

/* ------------------ Page buttons --------------------- */
#page-button {
  margin: 0.5rem;
  padding: 0.5rem 1rem;
  background-color: #f2f2f2;
  border: none;
  border-radius: 4px;
  font-family: "Roboto", sans-serif;
  font-size: 16px;
  cursor: pointer;
}

#page-button:hover {
  background-color: #e5e5e5;
}

/* --------------- Filter section ------------------- */
.filter-section {
  display: flex;
  justify-content: center;
  align-items: center;
  flex-wrap: wrap;
}

.filter-section>* {
  margin: 0 10px;
}

.alert {
  margin-bottom: 70px !important;
}

.unstyled-button {
  border: none;
  padding: 0;
  background: none;
}

#tuto p {
  margin: 0;
  padding: 0;
}

#tuto {
  padding-bottom: 12px;
}

.logwarn {
  font-size: smaller;
  color: rgb(226, 133, 141);
}

.filter-section label {
  font-size: smaller;
  color: rgb(133, 164, 226);
}

/* --------------- Event modal ------------------- */
.modal {
  display: block;
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  z-index: 9999;
}

.modal-content {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background-color: #fff;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.3);
  max-width: 90%;
  max-height: 90%;
  overflow-y: auto;
  overflow-x: hidden;
  /* Prevent horizontal scrolling on mobile */
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.modal-title {
  margin: 0;
  font-weight: bold;
}

.modal-body {
  display: flex;
  flex-wrap: wrap;
  display: flex;
}

.modal-infos {
  max-width: 40%;
  min-width: 600px;
}

.modal-description {
  text-align: justify;
  text-justify: inter-word;
  padding-left: 2em;
  padding-right: 2em;
}

.close {
  background-color: transparent;
  border: none;
  cursor: pointer;
  font-size: 24px;
}

.modal-event-image {
  width: 650px;
  height: 600px;
  object-fit: cover;
  object-position: center;
  margin-bottom: 20px;
  border-radius: 5px;
}

.modal-body {
  text-align: left;
  font-size: 18px;
  display: flex;
  justify-content: space-around;
}

.modal-label {
  font-weight: bold;
  display: inline-block;
  width: 150px;
  padding-left: 36px;
}

.modal-value {
  display: inline-block;
}

#msgDate {
  font-size: x-small;
  color: rgb(133, 164, 226);
  text-align: center;
  font-weight: bold;
}

@media only screen and (min-width: 1750px) {
  .modal-event-image {
    width: 850px;
    height: 600px;
    object-fit: cover;
    object-position: center;
    margin-bottom: 20px;
    border-radius: 5px;
  }
}

@media only screen and (max-width: 1500px) {
  .modal-event-image {
    width: 450px;
    height: 600px;
    object-fit: cover;
    object-position: center;
    margin-bottom: 20px;
    border-radius: 5px;
  }

  .modal-infos {
    max-width: 40%;
    min-width: 450px;
  }
}

@media only screen and (max-width: 600px) {
  .modal-event-image {
    width: 300px;
    height: auto;
    object-fit: cover;
    object-position: center;
    margin-bottom: 20px;
    border-radius: 5px;
  }

  .filter-section {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    margin: 0 0px;
    flex-wrap: wrap;
  }
}
</style>
