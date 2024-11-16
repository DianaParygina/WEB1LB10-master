<script setup>
import { useRoute } from 'vue-router';
import {computed, ref, onBeforeMount} from 'vue';

import useUserState from '../../stores/userStore';

const username = ref("");
const pass = ref("");
const userStore = useUserState();
const router=useRouter();
const{
    isAuthenticated
} = storeToRefs(userStore)

async function login(){
    const r = await axios.post("/api/user/login/", {
        user: username.value,
        pass: pass.value
    })
    await userStore.fetchUser();

    if (isAuthenticated.value){
        router.push("/")
    }
}

</script>


<template>


<input v-model="username">
<input type="password" v-model="pass">
<button @click="login"></button> 

</template>