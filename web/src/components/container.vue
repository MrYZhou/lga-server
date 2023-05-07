<template>
  <!-- 主布局 -->
    <div class="larry">

        <el-row :gutter="20" style="justify-content:center">
            <el-col :span="12">
                <el-input v-model="name" maxlength="10" show-word-limit></el-input>
            </el-col>
            <el-col :span="4">
                <el-button :icon="Search" type="primary" @click="showAdd">search</el-button>
                <el-button :icon="Plus" type="primary" @click="dialogFormVisible = true"></el-button>
            </el-col>
        </el-row>
        <el-dialog v-model="dialogFormVisible" title="task config">
            <el-form :model="form" style="">
                <el-form-item :label-width="'120px'" label="Promotion name">
                    <el-input v-model="form.name" autocomplete="off"/>
                </el-form-item>
                <el-form-item :label-width="'120px'" label="Zones">
                    <el-select v-model="form.type" placeholder="Please select a zone">
                        <el-option label="Zone No.1" value="shanghai"/>
                        <el-option label="Zone No.2" value="beijing"/>
                    </el-select>
                </el-form-item>
                <el-form-item :label-width="'120px'" label="脚本内容" style="height: 300px">
                    <code-panel ref="codecom" v-model:value="form.content" @valueRefresh="parse"></code-panel>
                </el-form-item>

            </el-form>
            <template #footer>
      <span class="dialog-footer">
        <el-button @click="dialogFormVisible = false">Cancel</el-button>
        <el-button type="primary" @click="dialogFormVisible = false">
          Confirm
        </el-button>
      </span>
            </template>
        </el-dialog>

        <el-row class="mt10">

            <!--            <el-card class="box-card">-->
            <!--            </el-card>-->
        </el-row>
    </div>
</template>
<script setup>
import {Plus, Search} from '@element-plus/icons-vue'
import {useMainStore} from "../store/index.js";
import CodePanel from "@/components/codePanel.vue";

const lar = inject("http")

lar.get('/task/add').then(res => {
    console.log(res)
})
const dialogFormVisible = ref(false)
let form = reactive({
    name: '',
    type: '',
    content: '',
})
const store = useMainStore();
let data = reactive({value2: "", value1: ""});
let timer = ref("");
let name = ref("")
let codecom = ref()
const parse = (val) => {

}
onUnmounted(() => {
    clearInterval(timer);
});

const showAdd = () => {

}
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
    /*display: flex;*/
    /*justify-content: space-between;*/
    /*min-width: 990px;*/
    width: 100%;
    height: calc(100vh - 50px);
    overflow-y: hidden;

}

.larry::-webkit-scrollbar {
    display: none;
}

.box-card {
    width: 300px;
    height: 300px;

}

</style>
