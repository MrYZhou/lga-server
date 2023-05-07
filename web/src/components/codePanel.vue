<template>
    <div v-if="show" ref="editContainer2" class="code-editor"></div>
</template>
<script>
import {getCurrentInstance, onMounted, watch} from "vue";
import * as monaco from "monaco-editor/esm/vs/editor/editor.main.js";
import JsonWorker from "monaco-editor/esm/vs/language/json/json.worker?worker";
// 解决vite Monaco提示错误
self.MonacoEnvironment = {
    getWorker() {
        return new JsonWorker();
    },
};
export default {
    props: {
        value: String,
    },
    data() {
        return {
            show: true,
        };
    },
    setup(props, {emit}) {
        let monacoEditor = null;
        const {proxy} = getCurrentInstance();

        watch(
            () => props.value,
            (value) => {
                // 防止改变编辑器内容时光标重定向
                if (value !== monacoEditor?.getValue()) {
                    monacoEditor.setValue(value);
                }
            },
            {deep: true}
        );
        const hide = () => (show = false);
        onMounted(() => {
            nextTick(() => {
            });
            monacoEditor = monaco.editor.create(proxy.$refs.editContainer2, {
                value: props.value, // 内容
                readOnly: false, // 是否只读
                language: "java", // 显示的语言
                foldingStrategy: "indentation", // 代码可分小段折叠
                automaticLayout: true, // 自适应布局
                theme: "vs", // 白色主题
                overviewRulerBorder: false, // 不要滚动条的边框
                autoClosingBrackets: true,
                selectOnLineNumbers: true,
                renderSideBySide: false,
                minimap: {
                    enabled: true, // 导航地图
                },
            });
            // 监听值变化
            monacoEditor.onDidChangeModelContent(() => {
                const currenValue = monacoEditor?.getValue();
                emit("update:value", currenValue);
            });
        });
        return {hide};
    },
};
</script>
<style scoped>
.code-editor {
    width: 100%;
    height: 100%;
}
</style>
