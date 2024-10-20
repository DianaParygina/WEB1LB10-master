<script setup>
import {computed, ref, onBeforeMount} from 'vue';
import axios from "axios";
import Cookies from 'js-cookie';

const breed = ref({});
const breedToEdit = ref({});
const breedToAdd = ref({});

const loading = ref(false); 


async function fetchBreeds(){
  const r = await axios.get("/api/breed/");
  console.log(r.data)
  breed.value = r.data;
}


async function onLoadClickForBreed(){
  await fetchBreeds()
}



async function onDogClickForBreeds(){
  await axios.post("/api/breed/", {
    ...breedToAdd.value,
  });
  await fetchBreeds(); // переподтягиваю
  breedToAdd.value = {};
}

async function onRemoveClickForBreed(breed) {
  await axios.delete(`/api/breed/${breed.id}/`);
  await fetchBreeds();
}


async function onBreedEditClick(breed) {
  breedToEdit.value = { ...breed }; 
}


async function onUpdateBreed() {
  await axios.put(`/api/breed/${breedToEdit.value.id}/`, {
    ...breedToEdit.value,
  });
  await fetchBreeds(); 
}




onBeforeMount(() => {
  axios.defaults.headers.common['X-CSRFToken'] = Cookies.get("csrftoken");
})

</script>

<template>
  <div><br>
    <button @click="onLoadClickForBreed">Загрузить породы собак</button>

    <div v-for="b in breed" class="breed-item">
      <div>{{ b.name }}</div>
      <button class="btn btn-success" @click="onBreedEditClick(b)" data-bs-toggle="modal" data-bs-target="#editDogModal2"> 
        <i class="bi bi-pen-fill"></i>
      </button>
      <button class="btn btn-danger" @click="onRemoveClickForBreed(b)">
        <i class="bi bi-x"></i>
      </button>
    </div>

    <form @submit.prevent.stop="onDogClickForBreeds">
      <div class="row">
        <div class="col-auto">
        <div class="form-floating">
            <input
              type="text"
              class="form-control"
              v-model="breedToAdd.name"
              required
            />
            <label for="floatingInput">Добавим породу</label>
          </div>
        </div>
        <div class="col-auto">
          <button class="btn btn-primary">
            Добавить
          </button>
        </div>
      </div>
    </form>

    <div class="modal fade" id="editDogModal2" tabindex="-1">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h1 class="modal-title fs-5" id="exampleModalLabel">
              Редактировать породу
            </h1>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <div class="row">
              <div class="col">
                <div class="form-floating">
                  <input type="text" class="form-control" v-model="breedToEdit.name" />
                  <label for="floatingInput">Порода</label>
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
            <button type="button" class="btn btn-primary" @click="onUpdateBreed" data-bs-dismiss="modal">
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
