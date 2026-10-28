<template>
    <div>
        生命周期（钩子函数）
    </div>


</template>
<script lang="ts" setup>
    import { 
        onBeforeMount, 
        onMounted, 

        // 组件卸载之前
        onBeforeUnmount,
        // 组件卸载之后
        onUnmounted,  
        // 数据更新之前
        onBeforeUpdate, 
        // 数据更新之后 
        onUpdated 
        
    } from 'vue'
    function show(){
        console.log('12345')
        // 调接口
    }
    onBeforeMount(()=>{
        console.log('组件挂载前，页面组件加载完成之前')
        // 一般在这个阶段 可以调用页面的初始化方法
        show()
    })
    onMounted(()=>{
        console.log('组件挂载完成，页面组件加载完成之后')
        // 可以在这调取初始化方法 可以操作页面的html元素
    })
</script>
