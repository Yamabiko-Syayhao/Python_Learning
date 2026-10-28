<!-- 写html的放template标签中 -->
<template>
  <div class="about">
    <p>
      <!-- 非表单元素使用插值渲染 {{ 变量名 }} -->
      {{ msg }}
    </p>
    <!-- 表单元素 v-model指令 -->
     <input type="text" v-model="msg">
     
     <!-- 双向绑定 -->
     <!-- 实现表单单选效果 v-model="sex" 当变量sex的值和value相同时，会自动选中，同样的当鼠标点击单选
      按钮时候，变量sex的值会自动改变为value的值。自动更新变量sex的值 -->
     <input type="radio" name="sex1" value="男" v-model="sex">男
     <input type="radio" name="sex1" value="女" v-model="sex">女
    
     <p>
      姓名是：{{ list1.name }}
      <br>
      爱好是：{{ list1.hobby }}
     </p>
     <!-- v-show 根据表达式的值来显示和隐藏元素 -->
     <!-- 一定会加载，只不过改变了样式display:none -->
      <!-- 相当于，v-show的值是isOK那么就是绑定下面定义的变量isOK的值
       也就是说isOK的值为true，就会显示元素，否则就会隐藏元素
       比如isOK1就不是isOK的值，所以不会显示元素 -->
     <h5 v-show="isOK1">今天周一清醒一下</h5>
     <!-- vi-if 根据表达式的真假来判断元素是否加载 v-else -->
      <h5 v-if="isOK1">晚上早点睡，白天别崩溃</h5>
      <h5 v-else>明天降温了</h5>
      <!-- v-bind用来绑定属性元素
       简写成 
       v-bind:属性名="变量" -->
       <!-- title属性绑定让鼠标悬停在元素上显示提示信息，而
        绑定的提示信息就是下面定义的byebye的值bysame -->
       <p v-bind:class="byebye":title="byebye">
        v-bind展示
       </p>
       <!-- 如果没用v-bind，那么title属性的值就是byebye的值,
        也就是说title最后显示的就是byebye，而不是bysame -->
       <h6 title="byebye">
        title展示2
       </h6>
  </div>
</template>
<!-- 创建一个组件---配置路由---加一个router-link跳转 -->

<!-- 写js就放script标签中 -->
 <!-- setup 是vue3的语法糖，用于在组件中使用js代码 -->
<!-- 必须加上 setup 关键字，否则会报错 -->
<script lang="ts" setup>
import { ref, reactive } from 'vue';
// 定义变量 使用let定义
// ref 定义了一个响应式变量
let msg = ref('hello vue3')
let sex = ref('男')
let list1 = reactive(
  {
    name: '张三',
    hobby: '打篮球'
  }
)
let isOK = ref(true)
let isShow = ref(true)
let byebye = ref("byesame")
</script>

<!-- 写样式就放style标签中 加scoped让样式只在当前组件中生效 
 避免组件污染 -->
<style scoped>
.byesame{
  color: red;
}
</style>
