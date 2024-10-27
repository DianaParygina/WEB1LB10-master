<script setup>
import { computed, ref, onBeforeMount } from 'vue';
import axios from "axios";
import Cookies from 'js-cookie';

const dogs = ref([]);
const dogToAdd = ref({});
const dogToEdit = ref({});
const dogsPicturesRef = ref({});
const dogsEditPicturesRef = ref({});
const dogAddImageUrl = ref();
const dogEditImageUrl = ref();
const showModal = ref(false);
const selectedImage = ref(null);

const breed = ref([]);
const owner = ref([]);
const country = ref([]);
const hobby = ref([]);

const loading = ref(false);

async function fetchDogs() {
  loading.value = true;
  const r = await axios.get("/api/dogs/");
  console.log(r.data)
  dogs.value = r.data;
  loading.value = false;
}

async function fetchBreeds() {
  const r = await axios.get("/api/breed/");
  console.log(r.data)
  breed.value = r.data;
}

async function fetchOwner() {
  const r = await axios.get("/api/owner/");
  console.log(r.data)
  owner.value = r.data;
}

async function fetchHobby() {
  const r = await axios.get("/api/hobby/");
  console.log(r.data)
  hobby.value = r.data;
}

async function fetchCountry() {
  const r = await axios.get("/api/country/");
  console.log(r.data)
  country.value = r.data;
}

async function dogsAddPictureChange() {
  dogAddImageUrl.value = URL.createObjectURL(dogsPicturesRef.value.files[0])
}

async function dogsEditPictureChange() {
  dogEditImageUrl.value = URL.createObjectURL(dogsEditPicturesRef.value.files[0])
}

async function onLoadClick() {
  await fetchDogs()
}



async function onDogAdd() {
  const formData = new FormData();

  formData.append('picture', dogsPicturesRef.value.files[0]);

  formData.set('name', dogToAdd.value.name)
  formData.set('breed', dogToAdd.value.breed.id);
  formData.set('owner', dogToAdd.value.owner.id);
  formData.set('country', dogToAdd.value.country.id);
  formData.set('hobby', dogToAdd.value.hobby.id); 

  await axios.post("/api/dogs/", formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  });
  await fetchDogs(); // переподтягиваю
  // dogToAdd.value = {};
}


async function onRemoveClick(dog) {
  await axios.delete(`/api/dogs/${dog.id}/`);
  await fetchDogs();
}



async function onDogEditClick(dog) {
  dogToEdit.value = { ...dog };
}


async function onUpdateDog() {
  const formData = new FormData();

  if (dogsEditPicturesRef.value.files[0]) {
    formData.append('picture', dogsEditPicturesRef.value.files[0]);
  }

  dogEditImageUrl.value = null;
  formData.set('name', dogToEdit.value.name)
  formData.set('breed', dogToEdit.value.breed.id)
  formData.set('owner', dogToEdit.value.owner.id)
  formData.set('country', dogToEdit.value.country.id)
  formData.set('hobby', dogToEdit.value.hobby.id)

  await axios.put(`/api/dogs/${dogToEdit.value.id}/`, formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  });
  await fetchDogs(); // переподтягиваю
}



onBeforeMount(() => {
  axios.defaults.headers.common['X-CSRFToken'] = Cookies.get("csrftoken");
  fetchBreeds();
  fetchOwner();
  fetchCountry();
  fetchHobby();
})

</script>

<template>
  <div>
    <button @click="onLoadClick">Загрузить собак</button>

    <div v-for="dog in dogs" class="dog-item">
      <div>{{ dog.name }}</div>
      <div v-show="dog.picture" @click="showModal = true; selectedImage = dog.picture"><img :src="dog.picture"
          style="max-height: 60px;" data-bs-toggle="modal" data-bs-target="#pictureDogModal"></div>
      <button class="btn btn-success" @click="onDogEditClick(dog)" data-bs-toggle="modal"
        data-bs-target="#editDogModal">
        <i class="bi bi-pen-fill"></i>
      </button>
      <button class="btn btn-danger" @click="onRemoveClick(dog)">
        <i class="bi bi-x"></i>
      </button>
    </div>

    <form @submit.prevent.stop="onDogAdd">
      <div class="row">
        <div class="col">
          <div class="form-floating">
            <input type="text" class="form-control" v-model="dogToAdd.name" required />
            <label for="floatingInput">Имя</label>
          </div>
        </div>
        <div class="col">
          <div class="form-floating">
            <select name="" id="" class="form-select" v-model="dogToAdd.breed">
              <option :value="b.id" v-for="b in breed">{{ b.name }}</option>
            </select>
            <label for="floatingInput">Порода</label>
          </div>
        </div>
        <div class="col">
          <input class="form-control" type="file" ref="dogsPicturesRef" @change="dogsAddPictureChange">
        </div>
        <div class="col">
          <img :src="dogAddImageUrl" style="max-height:  60px;" alt="">
        </div>
        <div class="col">
          <div class="form-floating">
            <select name="" id="" class="form-select" v-model="dogToAdd.owner">
              <option :value="o.id" v-for="o in owner">{{ o.first_name }} {{ o.last_name }}</option>
            </select>
            <label for="floatingInput">Хозяин</label>
          </div>
        </div>
        <div class="col">
          <div class="form-floating">
            <select name="" id="" class="form-select" v-model="dogToAdd.country">
              <option :value="c.id" v-for="c in country">{{ c.country }}</option>
            </select>
            <label for="floatingInput">Страна</label>
          </div>
        </div>
        <div class="col">
          <div class="form-floating">
            <select name="" id="" class="form-select" v-model="dogToAdd.hobby">
              <option :value="h.id" v-for="h in hobby">{{ h.name_hobby }}</option>
            </select>
            <label for="floatingInput">Хобби</label>
          </div>
        </div>
        <div class="col-auto">
          <button class="btn btn-primary">
            Добавить
          </button>
        </div>
      </div>
    </form>

    <div class="modal fade" id="editDogModal" tabindex="-1"
      @hidden.bs.modal="dogsEditPicturesRef.value = null; dogEditImageUrl.value = null;">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h1 class="modal-title fs-5" id="exampleModalLabel">
              Редактировать собаку
            </h1>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <div class="row">
              <div class="col">
                <div class="form-floating">
                  <input type="text" class="form-control" v-model="dogToEdit.name" />
                  <label for="floatingInput">Имя</label>
                </div>
              </div>
              <div class="col">
                <div class="form-floating">
                  <select name="" id="" class="form-select" v-model="dogToEdit.breed">
                    <option :value="b.id" v-for="b in breed">{{ b.name }}</option>
                  </select>
                  <label for="floatingInput">Порода</label>
                </div>
              </div>
              <div class="col">
                <input class="form-control" type="file" ref="dogsEditPicturesRef" @change="dogsEditPictureChange">
              </div>
              <div class="col">
                <div class="form-floating">
                  <select name="" id="" class="form-select" v-model="dogToEdit.owner">
                    <option :value="o.id" v-for="o in owner">{{ o.first_name }} {{ o.last_name }}</option>
                  </select>
                  <label for="floatingInput">Хозяин</label>
                </div>
              </div>
              <div class="col">
                <div class="form-floating">
                  <select name="" id="" class="form-select" v-model="dogToEdit.country">
                    <option :value="c.id" v-for="c in country">{{ c.country }}</option>
                  </select>
                  <label for="floatingInput">Страна</label>
                </div>
              </div>
              <div class="col">
                <div class="form-floating">
                  <select name="" id="" class="form-select" v-model="dogToEdit.hobby">
                    <option :value="h.id" v-for="h in hobby">{{ h.name_hobby }}</option>
                  </select>
                  <label for="floatingInput">Хобби</label>
                </div>
              </div>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">
              Close
            </button>
            <button type="button" class="btn btn-primary" @click="onUpdateDog" data-bs-dismiss="modal">
              Сохранить
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>



  <div class="modal fade" id="pictureDogModal" tabindex="-1">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>
        <div class="modal-body">
          <div class="row">
            <img :src="selectedImage" style="width: 100%; display: block; margin-left: auto; margin-right: auto">
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped></style>
