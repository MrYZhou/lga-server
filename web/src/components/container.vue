<template>

  <!-- 主布局 -->
    <div class="larry">
        hello
    </div>
</template>
<script setup>
import {
    View,
    Tools,
    Download,
    Document,
    DocumentCopy,
    Dish,
} from "@element-plus/icons-vue";
import {useMainStore} from "@/store";
import {ElMessageBox} from "element-plus";

const store = useMainStore();
let data = reactive({value2: "", value1: ""});
let timer = ref("");


onUnmounted(() => {
    clearInterval(timer);
});
let splitState = ref(false);


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
const axios = inject("axios"); // inject axios
const doParse = async () => {
    if (data.value1.length == 0 && store.config.parseType != 4) {
        ElMessage({
            message: "没有要解析的字符",
            type: "warning",
        });
        return;
    }
    await parse();
};

const parse = async () => {
    let config = store.config;
    console.log(JSON.parse(config.renderData))
    let query = {
        type: config.engine,
        content: data.value1,
        params: JSON.parse(config.renderData)
    }
    let res = await axios.post(`http://127.0.0.1:8088/render`, query);
    // 如果是默认模式,为content
    if (config.parseType === '1') {
        config.datakey = ''
    }

    if (config.datakey) {
        let keyList = config.datakey.split(".");
        keyList.forEach((key) => {
            if (res.data.hasOwnProperty(key)) {
                res.data = res.data[key];
            }
        });
    }
    let value = res.data;
    if (typeof value === "string") {
        data.value2 = value;
        if (splitState) {
            postMessage(value);
        }
    }
};

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
