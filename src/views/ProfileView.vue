<template>
  <head>
    <title>ProfileView</title>
  </head>

  <!-- Page navigation, used to access the three subpages of profile -->
  <!-- # Profile  -->
  <!-- # Like     -->
  <!-- # Events   -->
  <div class="container">
    <nav class="navbar">
      <form class="form-inline">
        <button class="btn btn-outline-dark" type="button" @click="this.nav = 'Profile'" autofocus="autofocus">
          Profile
        </button>
        <button class="btn btn-outline-dark" type="button" @click="this.nav = 'Like'">Like</button>
        <button class="btn btn-outline-dark" type="button" @click="this.nav = 'Events'">
          My events
        </button>
      </form>
    </nav>
  </div>

  <!-- Only displays if user is logged in -->
  <div v-if="user">
    <div class="container">

      <!-- Profile ---------------------------------------------------------------->
      <div v-if="this.nav === 'Profile'">
        <!--Profile picture-->
        <img id="ppPreview" v-bind:src="userData.profilePic" />
        <button id="changeImage" @click="randomizeImage" class="btn btn-dark">Change image</button>
        <form @submit.prevent="onSubmit">
          <div class="form-row">
            <div class="form-group col">
              <label for="username">Username</label>
              <input type="text" class="form-control" id="username" v-model="userData.username"
                :placeholder="user.username" style="height: 58px" />
            </div>
            <div class="form-group col">
              <label for="email">Email</label>
              <input type="text" class="form-control" id="email" v-model="userData.email" :placeholder="user.email"
                style="height: 58px" />
            </div>
          </div>
          <div v-if="successMessage" class="alert alert-success" role="alert" id="successMessage">
            {{ successMessage }}
          </div>

          <div v-if="errorMessage" class="alert alert-danger" role="alert" id="errorMessage">
            {{ errorMessage }}
          </div>

          <router-link to="/"><button class="btn btn-outline-danger btn-lg">Cancel</button></router-link>
          <button type="submit" class="btn btn-outline-success btn-lg">Submit</button>
        </form>
      </div>
    </div>
    <!-- Profile ---------------------------------------------------------------->

    <!-- Like ------------------------------------------------------------------->
    <div v-if="this.nav === 'Like'" class="container">
      <h1>Events you liked</h1>
      <div class="row g-3">
        <div class="col-12 col-md-6 col-lg-4" v-for="event in paginatedEvents" :key="event.id">
          <div class="card" @click="showEventDetails(event)">
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
            </div>
          </div>
        </div>
      </div>
      <button v-for="page in totalPages" :key="page" @click="changePage(page)" id="page-button">
        {{ page }}
      </button>
    </div>
    <!-- Like ------------------------------------------------------------------->

    <!-- Events ----------------------------------------------------------------->
    <div v-if="this.nav === 'Events'" class="container">
      <h1>Events you created</h1>
      <div class="row g-3">
        <div class="col-12 col-md-6 col-lg-4" v-for="event in paginatedEvents" :key="event.id">
          <div class="card" @click="showEventDetails(event)">
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
              <button class="btn btn-danger" @click="deleteEvent(event.id)" style="margin-top: 10px">
                Delete
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Page buttons -->
      <button v-for="page in totalPages" :key="page" @click="changePage(page)" id="page-button">
        {{ page }}
      </button>

      <!-- Success/Error messages -->
      <div v-if="successMessage" class="alert alert-success" role="alert" id="successMessage">
        {{ successMessage }}
      </div>

      <div v-if="errorMessage" class="alert alert-danger" role="alert" id="errorMessage">
        {{ errorMessage }}
      </div>
    </div>
    <!-- Events ----------------------------------------------------------------->

  </div>
</template>

<script>
import userService from "../services/userService"
import authService from "../services/authService"
import interestedService from "../services/interestedService"
import eventService from "../services/eventService"
import moment from "moment"

export default {
  data() {
    return {
      // Stores current user data, also used to update user data
      userData: {
        email: "",
        profilePic: "https://api.multiavatar.com/xxxx.svg",
        username: ""
      },

      // Messages used to display response from API calls
      successMessage: "",
      errorMessage: "",

      // nav let vue know what div to display, either "Profile", "Like" or "Events"
      nav: "Profile",
      currentPage: 1,
      itemsPerPage: 9
    }
  },

  async mounted() {

    await userService.fetchUsers()

    this.userData = userService.customUser.value

    await eventService.fetchEvents()

    // Allows the vue to stay on either "Profile", "Like" or "Events" in case of reload
    if (localStorage.getItem("currentNav")) {
      this.nav = localStorage.getItem("currentNav")
      localStorage.removeItem("currentNav")
    }
  },

  computed: {
    user() {
      return authService.user.value
    },

    customUser() {
      return userService.customUser.value
    },

    //Returns all the events the current user is interested in
    interestingEvents() {
      let interestingEventIds = [...interestedService.interestingEvent.value].map((e) => e.event)
      return [...eventService.events.value].filter((e) => interestingEventIds.includes(e.id))
    },

    //Returns all the events that were created by the current user
    createdEvents() {
      return [...eventService.events.value].filter((e) => e.creator.username == this.user.username)
    },

    //Returns the events that should be displayed on the current page, either "Like" or "Events"
    paginatedEvents() {
      const startIndex = (this.currentPage - 1) * this.itemsPerPage
      const endIndex = startIndex + this.itemsPerPage
      let sortedEvents
      if (this.nav === "Like") {
        sortedEvents = this.sortEventsByDate(this.interestingEvents)
      } else {
        sortedEvents = this.sortEventsByDate(this.createdEvents)
      }
      return sortedEvents.slice(startIndex, endIndex)
    },

    // Function that returns the total number of pages for displaying events
    totalPages() {
      if (this.nav === "Like") {
        return Math.ceil(this.interestingEventsLength / this.itemsPerPage)
      } else {
        return Math.ceil(this.createdEventsLength / this.itemsPerPage)
      }
    },

    interestingEventsLength() {
      return this.interestingEvents.length
    },

    createdEventsLength() {
      return this.createdEvents.length
    },
  },

  methods: {
    onSubmit() {
      // Send userData to backend to PATCH using /src/services/userService.js
      userService
        .patchUser(this.user.pk, this.userData)
        .then(() => {
          // Display success message
          this.successMessage = "Profile updated successfully!"

          // Hide success message after 5 seconds
          setTimeout(() => {
            this.successMessage = ""
            window.location.reload()
          }, 5000)
        })
        .catch((error) => {
          console.log(error)
          // Display error message
          this.errorMessage = `Failed to update profile. ${error.message}`

          // Hide error message after 5 seconds
          setTimeout(() => {
            this.errorMessage = ""
          }, 5000)
        })

      // Clear all the fields of userData
      this.userData = {
        profilePic: "",
        username: "",
        email: ""
      }
    },

    // Randomizes the profile picture
    randomizeImage() {
      let apiImage = "https://api.multiavatar.com/"
      let random = (Math.random() + 1).toString(36).substring(7)
      let apiImageEnd = ".svg"
      this.userData.profilePic = apiImage + random + apiImageEnd
    },

    // Formats the date using moment.js
    formatDate(date) {
      return moment(date).format("DD MMMM YYYY - HH:mm") // Customize the format as needed
    },

    // TO DO this is a placeholder for actions when an event card is clicked in the profile view
    showEventDetails(event) {
      // TO DO implement event modal as a component to be able to use it in profile view
      console.log(event)
    },

    // Sorts events by date
    sortEventsByDate(events) {
      return events.slice().sort((a, b) => new Date(a.date) - new Date(b.date))
    },

    // Changes the current page
    changePage(page) {
      this.currentPage = page
    },

    // Deletes an event via src\services\eventService.js
    deleteEvent(event) {
      eventService
        .deleteEvent(event)
        .then(() => {
          // Display success message
          this.successMessage = "Event deleted successfully!"

          // Hide success message after 5 seconds
          setTimeout(() => {
            this.successMessage = ""
            localStorage.setItem("currentNav", this.nav)
            window.location.reload()
          }, 3000)
        })
        .catch((error) => {
          console.log(error)
          // Display error message
          this.errorMessage = `Failed to update profile. ${error.message}`

          // Hide error message after 5 seconds
          setTimeout(() => {
            this.errorMessage = ""
          }, 5000)
        })
    }
  }
}
</script>

<style scoped>
/* ------------------ Update profile form ------------------ */
form {
  margin: 0px;
  padding: 0 5px;
}

.form-row {
  display: flex;
  flex-direction: row;
  margin: 0px;
  padding: 0px;
}

.form-group {
  margin: 10px;
  padding: 0px;
}

button {
  margin: 10px;
}

#ppPreview {
  max-width: 16vw;
}

/* ------------------ Event cards ------------------ */
.card-img-top {
  object-fit: cover;
  height: 300px;
  /* Adjust the height as needed */
  transition: transform 0.5s ease;
}

.card-img-container {
  overflow: hidden;
  height: 300px;
  /* Adjust the height as needed */
}

.card-img-container:hover .card-img-top {
  transform: scale(1.1);
}

.card-body {
  /*    height: 320px;*/
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
</style>
