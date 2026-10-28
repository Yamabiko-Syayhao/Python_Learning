<template>
  <h2>v-for</h2>
    <!-- 
    想生成谁 就给谁加上v-for
    v-for="(item,index) in 变量":key="index"
    item代表每一项的值 index就代表下标  
    -->
  <p v-for="(item,index) in arr" :key="index">
    {{index}}-----{{item.name}}
  </p>
</template>

<script lang="ts" setup>
    import{ref}from"vue"
    // ref 可以定义一个复杂数据类型的响应式
    let arr = ref([
        {
            name:"张三",
            age:18
        },
        {
            name:"李四",
            age:19
        },
        {
            name:"王五",
            age:20
        }
        
    ])
</script>



