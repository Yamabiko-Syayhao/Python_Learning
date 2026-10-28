<template>
        <h3>axios</h3>
        http://axios.org.cn/docs/intro
        <p>
            axios是一个基于Promise的HTTP库，用于浏览器和Node.js中发送HTTP请求。
            要先下载
        </p>
        <input type="text" placeholder="请输入用户名" v-model="obj.userName">
        <input type="password" placeholder="请输入密码" v-model="obj.passWord">
        <button @click="handleLogin1()">登录</button>
        <!-- 用户在输入账号密码之后点击登录按钮就可以取调取自己写的
         登录接口，登录成功之后将后端返回来的token存到本地缓存里面 -->
        <p>
            展示一下后端返回的userName---{{msg}}
        </p>

        <div>
        <input type="text" v-model="abc.c">
        {{ abc.c }}
        <button @click="handle2()">点击更新</button>
    </div>

    <div>
        展示res---{{ res }}
        <input type="text" v-model="res.aaa">
        <button @click="handle3()">点击更新res</button>
    </div>

</template>


<script lang="ts" setup>
import {ref,onMounted,reactive} from 'vue'
// 引入axios
import axios from 'axios'
let obj = ref({
    userName:"admin",
    passWord:"123456"
})

let handleLogin = ()=>{
    // 登录接口
    fetch('http://127.0.0.1:8000/api/login',{
        method:'POST',
        headers:{
            'Content-Type':'application/x-www-form-urlencoded'
        },
        body:`userName=${obj.value.userName}&passWord=${obj.value.passWord}`
    }).then(res=>res.json())
    .then((data)=>{//后端返回的数据
        console.log(data,"登录成功了")
        //将请求成功的数据返回到
        msg.value = data
    })
}
let msg = ref({})
// dom加载完成之后 也就是组件全部加载完成
onMounted(()=>{
    // 调用函数
    handleLogin()
})


let handleLogin1 = ()=>{
    // 登录接口 用axios
    // axios.post(url,data(请求头之类的),config(then((res)=>{})))
    axios.post('http://127.0.0.1:8000/api/login',{
        userName:obj.value.userName,
        passWord:obj.value.passWord
    },{
        headers:{
            'Content-Type':'application/x-www-form-urlencoded'
        }
    }).then((res)=>{
        console.log(res,"登录成功了")
        // console.log(res.data.token,"token")
        localStorage.setItem('token',res.data.token)
        msg.value = res
    })
}

onMounted(()=>{
    // 调用函数
    handleLogin1()
})


let abc = reactive({
        a:"admin",
        b:"1234",
        c:66
    })
    let handle2 = ()=>{
        // 通过reactive定义的响应式数据 可以直接修改数据 不需要加.value
        abc.c++
    }

    let res = reactive({})
    let handle3 = ()=>{
        // 破坏了原来的响应式
        // res = {
        //     aaa:666
        // }

        // 正确的赋值方式
        Object.assign(res,{
            aaa:666
        })
    }
</script>



