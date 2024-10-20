<script setup>
import {computed, ref, onBeforeMount} from 'vue';
import axios from "axios";
import Cookies from 'js-cookie';

const country = ref({});
const countryToEdit = ref({});
const countryToAdd = ref({});

const loading = ref(false); 

async function fetchCountry(){
  const r = await axios.get("/api/country/");
  console.log(r.data)
  country.value = r.data;
}

async function onLoadClickForBreedCountry(){
  await fetchCountry()
}

async function onDogClickForCountry(){
  await axios.post("/api/country/", {
    ...countryToAdd.value,
  });
  await fetchCountry(); // переподтягиваю
  countryToAdd.value = {};
}

async function onRemoveClickForCountry(country) {
  await axios.delete(`/api/country/${country.id}/`);
  await fetchCountry();
}


async function onCountryEditClick(country) {
  countryToEdit.value = { ...country }; 
}

async function onUpdateCountry() {
  await axios.put(`/api/country/${countryToEdit.value.id}/`, {
    ...countryToEdit.value,
  });
  await fetchCountry(); 
}

onBeforeMount(() => {
  axios.defaults.headers.common['X-CSRFToken'] = Cookies.get("csrftoken");
})

</script>

<template>
  <div><br>
    <button @click="onLoadClickForBreedCountry">Загрузить страны собак</button>

    <div v-for="c in country" class="country-item">
      <div>{{ c.country }}</div>
      <button class="btn btn-success" @click="onCountryEditClick(c)" data-bs-toggle="modal" data-bs-target="#editDogModal4"> 
        <i class="bi bi-pen-fill"></i>
      </button>
      <button class="btn btn-danger" @click="onRemoveClickForCountry(c)">
        <i class="bi bi-x"></i>
      </button>
    </div>

    <form @submit.prevent.stop="onDogClickForCountry">
      <div class="row">
        <div class="col-auto">
        <div class="form-floating">
            <input
              type="text"
              class="form-control"
              v-model="countryToAdd.country"
              required
            />
            <label for="floatingInput">Добавим страну</label>
          </div>
        </div>
        <div class="col-auto">
          <button class="btn btn-primary">
            Добавить
          </button>
        </div>
      </div>
    </form>

    <div class="modal fade" id="editDogModal4" tabindex="-1">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h1 class="modal-title fs-5" id="exampleModalLabel">
              Редактировать страну
            </h1>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <div class="row">
              <div class="col">
                <div class="form-floating">
                  <input type="text" class="form-control" v-model="countryToEdit.country" />
                  <label for="floatingInput">Страна</label>
                </div>
              </div>
              <div class="col">
        </div>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">
              Close
            </button>
            <button type="button" class="btn btn-primary" @click="onUpdateCountry" data-bs-dismiss="modal">
              Сохранить
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>


<style scoped>
</style>
