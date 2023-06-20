<template>
  <div class="container">
    <footer
      class="d-flex flex-wrap justify-content-between align-items-center py-3 my-4 border-top"
    >
      <!-- Back to top -->
      <div class="col-md-4 d-flex align-items-center">
        <a href="#" class="mb-3 me-2 mb-md-0 text-body-secondary text-decoration-none lh-1">
          <img src="../assets/hello-world-black.png" alt="helloworld" height="80" />
        </a>
        <span class="mb-3 mb-md-0 text-body-secondary">&copy; 2023 Hello World</span>
      </div>

      <ul class="nav col-md-4 justify-content-end list-unstyled d-flex">
        <!-- Acknowledgment trigger button-->
        <li class="ms-3">
          <a
            type="button"
            class="text-body-secondary"
            data-bs-toggle="modal"
            data-bs-target="#authorsModal"
            ><font-awesome-icon icon="fa-solid fa-square-plus" size="2xl" style="color: #000000"
          /></a>
        </li>

        <li class="ms-3">
          <a class="text-body-secondary" href="https://www.twitter.com"
            ><font-awesome-icon
              icon="fa-brands fa-square-twitter"
              size="2xl"
              style="color: #000000"
          /></a>
        </li>

        <li class="ms-3">
          <a class="text-body-secondary" href="https://www.instagram.com"
            ><font-awesome-icon
              icon="fa-brands fa-square-instagram"
              size="2xl"
              style="color: #000000"
          /></a>
        </li>

        <li class="ms-3">
          <a
            class="text-body-secondary"
            href="https://www.github.com/heg-interschool/project-helloworld"
            ><font-awesome-icon icon="fa-brands fa-square-github" size="2xl" style="color: #000000"
          /></a>
        </li>
      </ul>
    </footer>
  </div>

  <!-- Acknowledgment Modal -->
  <div
    class="modal fade"
    id="authorsModal"
    tabindex="-1"
    aria-labelledby="authorsModalLabel"
    aria-hidden="true"
  >
    <div class="modal-dialog modal-sm">
      <div class="modal-content">
        <div class="modal-header">
          <h1 class="modal-title fs-5" id="authorsModalLabel">Authors</h1>
          <button
            type="button"
            class="btn-close"
            data-bs-dismiss="modal"
            aria-label="Close"
          ></button>
        </div>
        <div class="modal-body">
          <div>
            <a href="https://www.github.com/boranuzun" class="text-decoration-none text-reset"
              >Boran UZUN</a
            >
          </div>
          <div>
            <a href="https://www.github.com/Gianou" class="text-decoration-none text-reset"
              >David GIANADDA</a
            >
          </div>
          <div>
            <a href="https://www.github.com/Fllet-sbxd" class="text-decoration-none text-reset"
              >Ian BRANDT</a
            >
          </div>
          <div>
            <a href="https://www.github.com/SzymonWojcik1" class="text-decoration-none text-reset"
              >Szymon WOJCIK</a
            >
          </div>
          <div>
            <a href="https://www.github.com/eleonorabiolo" class="text-decoration-none text-reset"
              >Eleonora BIOLO</a
            >
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "SiteFooter",

  data() {},
  computed: {},
  methods: {}
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped></style>
