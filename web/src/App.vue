<template>
    <div class="common-layout">
        <el-container style="overflow-y: hidden;">
            <el-main>
                <container/>
            </el-main>
        </el-container>
    </div>
</template>
<script setup>
import Container from "./components/container.vue";
</script>

<style scoped>
div.common-layout {
    height: 100%;
}
</style>
