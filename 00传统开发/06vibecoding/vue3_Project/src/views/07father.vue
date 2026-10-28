<template>
    <div class="father">
        <h3>父组件</h3>
        <button @click="handleToggle()">点击切换</button>
        <!-- 2.使用子组件 -->
        <!-- 3.在父组件内部的子组件标签上 绑定自定义属性，值就是你想传递给子组件的值-->
        <elSon :msg1="msg1" :msg2="msg2" @abc="handleA" @def="handleB" v-if="isOk"></elSon>
        <p>
            展示一下儿子的孝敬--{{ msg3 }}--{{ msg4 }}
        </p>
    </div>
</template>
<script lang="ts" setup>
    // 1.引入子组件   在这@代表src目录
    import elSon from "@/components/son.vue"

    import { ref } from "vue"
    let msg1 = ref("爸爸打你一巴掌")
    let msg2 = ref("爸爸踢了你一脚")

    let msg3 = ref("")
    let msg4 = ref("")
    // val 默认就是子组件传进来的数据
    let handleA = (val)=>{
        msg3.value = val
    }
    let handleB= (val)=>{
        msg4.value = val
    }

    let isOk = ref(true)
    let handleToggle = ()=>{
        // 点击一次 就让isOk的值取反
        isOk.value = !isOk.value
    }
</script>
<style scoped>
    .father{
        background-color: skyblue;
        padding: 20px;
    }
    h3{
        color: red;
    }
</style>
<!-- 
组件通信
    父子通信
        父传子：
        子传父
    非父子
 -->