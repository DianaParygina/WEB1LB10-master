<script setup>
import {computed, ref, onBeforeMount} from 'vue';
import axios from "axios";
import Cookies from 'js-cookie';

const hobby = ref({});
const hobbyToEdit = ref({});
const hobbyToAdd = ref({});

const loading = ref(false); 

async function fetchHobby(){
  const r = await axios.get("/api/hobby/");
  console.log(r.data)
  hobby.value = r.data;
}

async function onLoadClickForHobby(){
  await fetchHobby()
}


async function onDogClickForHobby(){
  await axios.post("/api/hobby/", {
    ...hobbyToAdd.value,
  });
  await fetchHobby(); // переподтягиваю
  hobbyToAdd.value = {};
}

async function onRemoveClickForHobby(hobby) {
  await axios.delete(`/api/hobby/${hobby.id}/`);
  await fetchHobby();
}


async function onHobbyEditClick(hobby) {
  hobbyToEdit.value = { ...hobby }; 
}

async function onUpdateHobby() {
  await axios.put(`/api/hobby/${hobbyToEdit.value.id}/`, {
    ...hobbyToEdit.value,
  });
  await fetchHobby(); 
}



onBeforeMount(() => {
  axios.defaults.headers.common['X-CSRFToken'] = Cookies.get("csrftoken");
})

</script>

<template>
    <div><br>
    <button @click="onLoadClickForHobby">Загрузить хобби собак</button>

    <div v-for="h in hobby" class="hobby-item">
      <div>{{ h.name_hobby }}</div>
      <button class="btn btn-success" @click="onHobbyEditClick(h)" data-bs-toggle="modal" data-bs-target="#editDogModal5"> 
        <i class="bi bi-pen-fill"></i>
      </button>
      <button class="btn btn-danger" @click="onRemoveClickForHobby(h)">
        <i class="bi bi-x"></i>
      </button>
    </div>

    <form @submit.prevent.stop="onDogClickForHobby">
      <div class="row">
        <div class="col-auto">
        <div class="form-floating">
            <input
              type="text"
              class="form-control"
              v-model="hobbyToAdd.name_hobby"
              required
            />
            <label for="floatingInput">Добавим хобби</label>
          </div>
        </div>
        <div class="col-auto">
          <button class="btn btn-primary">
            Добавить
          </button>
        </div>
      </div>
    </form>

    <div class="modal fade" id="editDogModal5" tabindex="-1">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h1 class="modal-title fs-5" id="exampleModalLabel">
              Редактировать хобби
            </h1>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <div class="row">
              <div class="col">
                <div class="form-floating">
                  <input type="text" class="form-control" v-model="hobbyToEdit.name_hobby" />
                  <label for="floatingInput">Хобби</label>
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
            <button type="button" class="btn btn-primary" @click="onUpdateHobby" data-bs-dismiss="modal">
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
