<template>
  <head>
    <title>Event creation</title>
  </head>
  <div>
    <div class="title">
      <h1 class="title">Event creation</h1>
      <hr />
    </div>
    <div v-if="user">
      <form @submit.prevent="onSubmit">
        <!-- Event name -->
        <div class="form-floating mb-3">
          <input type="text" class="form-control" id="floatingTitle" placeholder="Title" v-model="eventData.title"
            required />
          <label for="floatingTitle">Title</label>
        </div>

        <!-- Description -->
        <div class="form-floating mb-3">
          <textarea type="text" class="form-control" id="floatingDescription" placeholder="Description"
            v-model="eventData.description" style="height: 100px" required></textarea>
          <label for="floatingDescription">Description</label>
        </div>

        <!-- Event picture -->
        <div class="form-floating mb-3">
          <input type="url" class="form-control" id="floatingUrl" placeholder="www.example.com"
            v-model="eventData.event_pic" />
          <label for="floatingUrl">Event Picture (Link)</label>
        </div>

        <!-- Date and time -->
        <div class="form-row">
          <div class="form-floating mb-3 col">
            <input type="datetime-local" class="form-control" id="date" placeholder="Date and time of event"
              v-model="eventData.date" required />
            <label for="date" class="form-label">Date and time of event</label>
          </div>

          <!-- Capacity -->
          <div class="form-floating mb-3 col">
            <input type="number" class="form-control" id="event-cap" placeholder="Event capacity"
              v-model="eventData.event_capacity" required />
            <label for="event-cap" class="form-label">Event capacity</label>
          </div>

          <!-- Price -->
          <div class="form-floating mb-3 col">
            <input type="number" class="form-control" id="floatingPrice" placeholder="Price" v-model="eventData.price"
              required />
            <label for="floatingPrice" class="form-label">Price</label>
          </div>
        </div>

        <!-- Place -->
        <div class="form-floating col">
          <select class="form-select" id="floatingPlace" v-model="eventData.place" @change="handlePlaceSelection"
            required>
            <option selected disabled value="">Choose a place</option>
            <option value="create-new-place">--------- Create place ---------</option>
            <option v-for="place in places" :key="place.id" :value="place.id">
              {{ place.venue_name }}
            </option>
          </select>
          <label for="floatingPlace">List of places</label>
        </div>

        <!-- Success/Error messages -->
        <div v-if="successMessage" class="alert alert-success" role="alert" id="successMessage">
          {{ successMessage }}
        </div>

        <div v-if="errorMessage" class="alert alert-danger" role="alert" id="errorMessage">
          {{ errorMessage }}
        </div>

        <!-- Cancel/Submit buttons -->
        <router-link to="/"><button class="btn btn-outline-danger btn-lg">Cancel</button></router-link>
        <button type="submit" class="btn btn-outline-success btn-lg">Submit</button>
      </form>
    </div>
    <div v-else>
      <p>You have to login</p>
    </div>
  </div>
</template>

<script>
import eventService from "../services/eventService" // For creating event
import authService from "../services/authService" // For fetching currently logged in user's id
import placeService from "../services/placeService" // For fetching places
export default {
  name: "CreateEventView",
  data() {
    return {
      // Paylod to post an Event
      eventData: {
        title: "",
        description: "",
        event_pic: "",
        date: "",
        event_capacity: "",
        price: "",
        place: "",
        creator: null
      },

      successMessage: "",
      errorMessage: ""
    }
  },

  async mounted() {
    try {
      // Fetch places
      await placeService.fetchPlaces()

      // Set eventData.creator to currently logged in user's id
      this.eventData.creator = authService.user.value.pk
    } catch (error) {
      console.log(error)
    }
  },

  computed: {
    user() {
      return authService.user.value
    },

    places() {
      return placeService.places.value
    }
  },

  methods: {
    // Send eventData to backend to POST using /src/services/placeService
    onSubmit() {
      // Set default value for event_pic if not provided by the user
      if (!this.eventData.event_pic) {
        this.eventData.event_pic =
          "https://decizia.com/blog/wp-content/uploads/2017/06/default-placeholder.png"
      }
      // Convert eventData to JSON
      const eventDataJSON = JSON.stringify(this.eventData)

      // Send eventDataJSON to backend to create event using /src/services/eventService.js
      eventService
        .postEvent(eventDataJSON)
        .then(() => {
          // Display success message
          this.successMessage = "Event created successfully!"

          // Hide success message after 5 seconds
          setTimeout(() => {
            this.successMessage = ""
          }, 5000)
        })
        .catch((error) => {
          console.log(error)
          // Display error message
          this.errorMessage = `Failed to create event. ${error.message}`

          // Hide error message after 5 seconds
          setTimeout(() => {
            this.errorMessage = ""
          }, 5000)
        })

      // Clear all fields
      this.eventData = {
        title: "",
        description: "",
        event_pic: "",
        date: "",
        event_capacity: "",
        price: "",
        place: "",
        creator: this.eventData.creator // Keep creator id
      }
    },

    handlePlaceSelection() {
      if (this.eventData.place === "create-new-place") {
        // Redirect the user to the CreatePlaceView page
        window.location.href = "#/CreatePlaceView"
      }
    },
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
div {
  margin: 50px;
}

form {
  margin: 50px;
  padding: 0 5px;
}

.form-row {
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
  margin: 0px;
  padding: 0px;
}

.form-group+.form-row {
  margin-top: -50px;
}

button {
  margin: 10px;
}

.title {
  text-align: left;
}

@media only screen and (max-width: 1120px) {
  .form-row * {
    width: auto !important;
  }
}

@media only screen and (max-width: 600px) {
  .form-control {
    width: auto !important;
  }

  div {
    width: 100%;
    margin: 0;
    display: flex;
    flex-direction: column;
  }

  .title {
    text-align: center;
  }
}
</style>
