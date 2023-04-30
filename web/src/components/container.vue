<template>
  <!-- 主布局 -->
    <div class="larry">
        <div class="card">larry</div>

    </div>
</template>
<script setup>

import {useMainStore} from "../store/index.js";

const lar = inject("http")

lar.get('/task/add').then(res => {
    console.log(res)
})


const store = useMainStore();
let data = reactive({value2: "", value1: ""});
let timer = ref("");


onUnmounted(() => {
    clearInterval(timer);
});


const initListener = () => {
    window.addEventListener("message", function (event) {
        if (event.data?.type != "preview") {
            return;
        }
        data.value2 = event.data.msg;
    });
};

const loadConfig = () => {
    // 请求后端config配置

    let configData = localStorage.getItem("design-config");
    let config = JSON.parse(configData);
    if (configData) {
        store.saveConfig(config);
    }

};

watchEffect(() => {
});

onMounted(() => {

    initListener();

    loadConfig();

});

// 下载
const doDownload = () => {
};
</script>

<style scoped>
.larry {
    background-color: #f1f1f1;
    display: flex;
    justify-content: space-between;
    min-width: 990px;
    height: calc(100vh - 50px);
    overflow-y: hidden;

}

.larry::-webkit-scrollbar {
    display: none;
}

</style>
