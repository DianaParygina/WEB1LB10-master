<script setup>
import { computed, ref, onBeforeMount } from 'vue';
import axios from "axios";
import Cookies from 'js-cookie';

const owner = ref({});
const ownerToEdit = ref({});
const ownerToAdd = ref({});
const ownersPicturesRef = ref({});
const ownerAddImageUrl = ref();
const showModal = ref(false);
const selectedImage = ref(null);
const ownersEditPicturesRef = ref({});
const ownerEditImageUrl = ref();

const loading = ref(false);

async function fetchOwner() {
  loading.value = true;
  const r = await axios.get("/api/owner/");
  console.log(r.data)
  owner.value = r.data;
  loading.value = false;
}

async function ownersAddPictureChange() {
  ownerAddImageUrl.value = URL.createObjectURL(ownersPicturesRef.value.files[0])
}

async function ownersEditPictureChange() {
  ownerEditImageUrl.value = URL.createObjectURL(ownersEditPicturesRef.value.files[0])
}

async function onLoadClickForOwner() {
  await fetchOwner()
}


async function onDogClickForOwner() {
  const formData = new FormData();

  formData.append('pictureOwner', ownersPicturesRef.value.files[0]);

  formData.set('first_name', ownerToAdd.value.first_name)
  formData.set('last_name', ownerToAdd.value.last_name)
  formData.set('phone_number', ownerToAdd.value.phone_number)

  await axios.post("/api/owner/", formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  });
  await fetchOwner(); // переподтягиваю
  // ownerToAdd.value = {};
}


async function onRemoveClickForOwner(owner) {
  await axios.delete(`/api/owner/${owner.id}/`);
  await fetchOwner();
}

async function onOwnerEditClick(owner) {
  ownerToEdit.value = { ...owner };
}

async function onUpdateOwner() {

  const formData = new FormData();

  if (ownersEditPicturesRef.value.files[0]) {
    formData.append('pictureOwner', ownersEditPicturesRef.value.files[0]);
  }

  ownerEditImageUrl.value = null;
  formData.set('first_name', ownerToEdit.value.first_name.id)
  formData.set('last_name', ownerToEdit.value.last_name.id)
  formData.set('phone_number', ownerToEdit.value.phone_number.id)

  await axios.put(`/api/owner/${ownerToEdit.value.id}/`, formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  });
  await fetchOwner();
}



onBeforeMount(() => {
  axios.defaults.headers.common['X-CSRFToken'] = Cookies.get("csrftoken");
})

</script>

<template>
  <div><br>
    <button @click="onLoadClickForOwner">Загрузить хозяинов собак</button>

    <div v-for="o in owner" class="owner-item">
      <div>{{ o.first_name }} {{ o.last_name }}</div>
      <div v-show="o.pictureOwner" @click="showModal = true; selectedImage = o.pictureOwner"><img :src="o.pictureOwner"
          style="max-height: 60px;" data-bs-toggle="modal" data-bs-target="#pictureOwnerModal"></div>
      <button class="btn btn-success" @click="onOwnerEditClick(o)" data-bs-toggle="modal"
        data-bs-target="#editDogModal3">
        <i class="bi bi-pen-fill"></i>
      </button>
      <button class="btn btn-danger" @click="onRemoveClickForOwner(o)">
        <i class="bi bi-x"></i>
      </button>
    </div>

    <form @submit.prevent.stop="onDogClickForOwner">
      <div class="row">
        <div class="col-auto">
          <div class="form-floating">
            <input type="text" class="form-control" v-model="ownerToAdd.first_name" required />
            <label for="floatingInput">Имя хозяина</label>
          </div>
        </div>
        <div class="col-auto">
          <div class="form-floating">
            <input type="text2" class="form-control" v-model="ownerToAdd.last_name" required />
            <label for="floatingInput">Фамилия хозяина</label>
          </div>
        </div>
        <div class="col-auto">
          <div class="form-floating">
            <input type="text3" class="form-control" v-model="ownerToAdd.phone_number" required />
            <label for="floatingInput">Номер телефона хозяина</label>
          </div>
        </div>
        <div class="col">
          <input class="form-control" type="file" ref="ownersPicturesRef" @change="ownersAddPictureChange">
        </div>
        <div class="col">
          <img :src="ownerAddImageUrl" style="max-height:  60px;" alt="">
        </div>
        <div class="col-auto">
          <button class="btn btn-primary">
            Добавить
          </button>
        </div>
      </div>
    </form>

    <div class="modal fade" id="editDogModal3" tabindex="-1"
    @hidden.bs.modal="dogsEditPicturesRef.value = null; dogEditImageUrl.value = null;">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h1 class="modal-title fs-5" id="exampleModalLabel">
              Редактировать хозяина
            </h1>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <div class="row">
              <div class="col">
                <div class="form-floating">
                  <input type="text" class="form-control" v-model="ownerToEdit.first_name" />
                  <label for="floatingInput">Имя хозяина</label>
                </div>
              </div>
              <div class="col">
                <div class="form-floating">
                  <input type="text" class="form-control" v-model="ownerToEdit.last_name" />
                  <label for="floatingInput">Фамилия хозяина</label>
                </div>
              </div>
              <div class="col">
                <div class="form-floating">
                  <input type="text" class="form-control" v-model="ownerToEdit.phone_number" />
                  <label for="floatingInput">Телефон хозяина</label>
                </div>
              </div>
              <div class="col">
                <input class="form-control" type="file" ref="ownersEditPicturesRef" @change="ownersEditPictureChange">
              </div>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">
              Close
            </button>
            <button type="button" class="btn btn-primary" @click="onUpdateOwner" data-bs-dismiss="modal">
              Сохранить
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>


  <div class="modal fade" id="pictureOwnerModal" tabindex="-1">
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
