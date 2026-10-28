<template>
  <button @click="handle1()">查询英雄联盟图片</button>
    <div class="box">
        <div class="img_list" v-for="(item,index) in list" :key="index">
            <!-- <img class="imgs" :src="'https://game.gtimg.cn/images/lol/act/img/champion/'+item.alias +'.png'"> -->
            <img class="imgs" :src="`https://game.gtimg.cn/images/lol/act/img/champion/${item.alias}.png`">
            <p class="img_name">{{ item.name }}</p>
        </div>
    </div>
</template>

<script lang="ts" setup>
    import { ref,onMounted, reactive } from "vue"
    // 引入axios  引入之前一定要先下载
    import axios from "axios"
    let obj = ref({
        userName:"admin",
        passWord:"1234"
    })
    let msg = ref({})
    // let handleLogin = ()=>{
    //     // 调接口 用fetch  
    //     // 接口api  http://127.0.0.1:5000/api/login  
    //     // 请求方式 post   参数字段userName passWord   请求头 application/x-www-form-urlencoded
    //     fetch("http://127.0.0.1:5000/api/login",{
    //         method:"post",
    //         headers:{
    //             "Content-Type":"application/x-www-form-urlencoded"
    //         },
    //         body:`userName=${obj.value.userName}&passWord=${obj.value.passWord}`
    //     }).then((res)=>res.json())
    //     .then((data)=>{
    //         console.log(data,"后端返回的数据")
    //         // 将请求成功的数据赋值给msg这个变量
    //         msg.value = data
    //     })
    // }
    // dom加载完成之后  组件全部加载完成
    onMounted(()=>{
        // 调用函数
        handleLogin()
    })


    // 接口api  http://127.0.0.1:5000/api/login  
    // 请求方式 post   参数字段userName passWord   请求头 application/x-www-form-urlencoded
    let handleLogin = ()=>{
        // 调接口 用axios   
        // axios.post(url,data,{请求头之类的}).then((res)=>{})
        axios.post("http://127.0.0.1:5000/api/login",{
            userName:obj.value.userName,
            passWord:obj.value.passWord
        },{
            headers:{
                "Content-Type":"application/x-www-form-urlencoded"
            }
        }).then((res)=>{
            console.log(res,"后端返回的数据")
            // console.log(res.data.token,"token")
            localStorage.setItem("token",res.data.token)
        })
    }

    // 英雄联盟接口
    // 请求api: https://game.gtimg.cn/images/lol/act/img/js/heroList/hero_list.js?v=58
    // 请求方式get  参数无  回显的图片链接https://game.gtimg.cn/images/lol/act/img/champion/xxxx.png
    // xxxx是后端返回的alias
    let list:any = ref([])
    let handle1 = ()=>{
        axios({
            method:"get",
            url:"https://game.gtimg.cn/images/lol/act/img/js/heroList/hero_list.js?v=58"
        }).then((res)=>{
            console.log(res,"后端返回的数据")
            // 将后端返回给的  前端能用的数据 赋值给一个变量
            // 将来这个变量就可以去更新视图
            list.value = res.data.hero
        })
    }

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

<style scoped>
    .box{
        width: 1000px;
        margin: auto;
        border: 1px solid red;
        display: flex;
        justify-content: space-between;
        flex-wrap: wrap;
    }
    .imgs{
        width: 120px;
        height: 120px;
    }
    .img_name{
        text-align: center;
        padding: 10px 0;
    }
</style>