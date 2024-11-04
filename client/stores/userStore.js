import { onBeforeMount, ref } from "vue";
import axios from "axios";
import { defineStore } from "pinia";


const useUserState = defineStore("UserStore", ()=>{
    const isAuthenticated = ref(false);
    const userName = ref("");
    const userId = ref();

    async function fetchUser() {
        const r = await axios.get("/api/user/info/")
        isAuthenticated.value = r.data.is_authenticated;
        userName.value = r.data.userName;
        userId.value = r.data.userId;
    }

    onBeforeMount(()=> {
        fetchUser();
    })

    return{
        isAuthenticated,
        userName,
        userId,
        fetchUser
    }
})

export default useUserState