<template>
  <head>
    <title>Place creation</title>
  </head>
  <div>
    <div class="title">
      <h1 class="title">Place creation</h1>
      <hr />
    </div>
    <div v-if="user">
      <form @submit.prevent="onSubmit">
        <!-- Venue name -->
        <div class="form-floating mb-3">
          <input type="text" class="form-control" id="floating_venue_name" placeholder="Venue name"
            v-model="placeData.venue_name" required />
          <label for="floating_venue_name">Venue name</label>
        </div>

        <!-- Address -->
        <div class="form-floating mb-3">
          <input type="text" class="form-control" id="floatingAddress" placeholder="Address" v-model="placeData.address"
            required />
          <label for="floatingAddress">Address</label>
        </div>

        <!-- Zip -->
        <div class="form-row">
          <div class="form-floating mb-3 col">
            <input type="text" class="form-control" id="floatingZip" placeholder="Zip" v-model="placeData.zip" required />
            <label for="floatingZip">Zip</label>
          </div>

          <!-- City -->
          <div class="form-floating mb-3 col-4">
            <input type="text" class="form-control" id="floatingCity" placeholder="City" v-model="placeData.city"
              required />
            <label for="floatingCity">City</label>
          </div>

          <!-- State -->
          <div class="form-floating col-4">
            <input type="text" class="form-control" id="floatingState" placeholder="State" v-model="placeData.state"
              required />
            <label for="floatingState">State</label>
          </div>
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
import placeService from "../services/placeService" // For creating place
import authService from "../services/authService" // For fetching currently logged in user's id
export default {
  name: "CreatePlaceView",
  data() {
    return {
      // Paylod to post a Place
      placeData: {
        venue_name: "",
        address: "",
        zip: "",
        city: "",
        state: "",
        creator: null
      },

      successMessage: "",
      errorMessage: ""
    }
  },

  async mounted() {
    this.placeData.creator = authService.user.value.pk
  },

  computed: {
    user() {
      return authService.user.value
    }
  },

  methods: {
    // Send placeData to backend to POST using /src/services/placeService
    onSubmit() {
      placeService
        .postPlace(this.placeData)
        .then(() => {
          // Display success message
          this.successMessage = "Place created successfully!"

          // Hide success message after 5 seconds
          setTimeout(() => {
            this.successMessage = ""
          }, 5000)
        })
        .catch((error) => {
          console.log(error)
          // Display error message
          this.errorMessage = `Failed to create place. ${error.message}`

          // Hide error message after 5 seconds
          setTimeout(() => {
            this.errorMessage = ""
          }, 5000)
        })

      // Clear all fields
      this.placeData = {
        venue_name: "",
        address: "",
        zip: "",
        city: "",
        state: "",
        creator: this.placeData.creator // Keep creator
      }
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
div {
  margin: 50px;
  /* border: 1px solid rgb(196, 33, 33); */
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
