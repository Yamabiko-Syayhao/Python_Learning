<template>
    <div class="son">
        <h3>子组件</h3>
        <p>
            展示父亲的宠爱---{{ props.msg1 }}--{{ props.msg2 }}
        </p>
        <button @click="handleClick()">点击发送给父亲</button>
    </div>
</template>
<script lang="ts" setup>
    import { defineProps,ref,defineEmits } from "vue"
    // 4. 在子组件内部接收数据
    const props = defineProps({
        msg1:String,
        msg2:String
    })

    // 子传父开始
    let son1 = ref("儿子给爸爸买了桶泡面")
    let son2 = ref("儿子给爸爸买了根泡面伴侣")
    const emit = defineEmits(["abc","def"])
    let handleClick = ()=>{
        emit("abc",son1.value)
        emit("def",son2.value)
    }
</script>
/*

<style scoped>
    .son{
        background-color: orange;
    }
    h3{
        color: green;
    }
</style>