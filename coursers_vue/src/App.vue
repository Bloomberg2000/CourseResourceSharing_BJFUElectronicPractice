<template>
    <a-layout id="app" style="min-height: 100vh">
        <a-layout-sider collapsible v-model="collapsed">
            <!--            <div class="logo"/>-->
            <div class="logo">
                <img style="height: 32px" :src="imgpath.public.logo"/>
                <span class="logoText" v-show="!collapsed">课程共享平台</span>
            </div>
            <a-menu theme="dark" :defaultSelectedKeys="['1']" mode="inline">
                <a-menu-item key="1">
                    <a-icon type="schedule"/>
                    <span>选课系统</span>
                </a-menu-item>
                <a-menu-item key="2">
                    <a-icon type="team"/>
                    <span>友情链接</span>
                </a-menu-item>
                <a-sub-menu key="sub1">
                    <span slot="title"><a-icon type="user"/><span>个人中心</span></span>
                    <a-menu-item key="3">我的信息</a-menu-item>
                    <a-menu-item key="4">选课记录</a-menu-item>
                </a-sub-menu>
            </a-menu>
        </a-layout-sider>
        <a-layout>
            <a-layout-header style="background: #fff; padding: 0"/>
            <a-layout-content style="margin: 0 16px">
                <router-view/>
            </a-layout-content>
            <a-layout-footer style="text-align: center">
                课程共享平台 ©2018
            </a-layout-footer>
        </a-layout>
    </a-layout>
</template>
<script>
    export default {
        data() {
            return {
                collapsed: false,
            }
        },
        computed: {
            imgpath() {
                return this.$store.state.imageStyle;
            },
        }
    }
</script>

<style>
    #app .logo {
        height: 32px;
        margin: 21px;
    }

    .logo .logoText {
        font-size: 15px;
        color: #ffffff;
        padding: 10px;

    }
</style>
