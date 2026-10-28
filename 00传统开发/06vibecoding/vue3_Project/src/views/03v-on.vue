<template>
  <div>
    <p>
        name---{{obj.name}}
    </p>
    <input type="text" v-model="num">
    <p>
        obj---{{obj}}
    </p>
    <!-- 
        点击事件
        v-on:click="函数名()"
        简写为
        @click="函数名()"
    -->
    <button @click="handleClick">点击更新</button>
  </div>
</template>
<script lang="ts" setup>
import { ref } from 'vue'
let num = ref(0)
let obj = ref({
    name: '张三',
    age: 18
})
// 定义函数
// 相当于function handleClick(){}
let handleClick = ()=>{
    // ref定义的响应式数据 修改的时候
    num.value++
    obj.value.age++
}
</script>