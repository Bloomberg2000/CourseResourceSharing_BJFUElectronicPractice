<template>
    <div class="home">
        <div :style="{ background: '#fff', padding: '24px', minHeight: '500px', textAlign:'center'}">
            <a-carousel dotsClass="slick-dots slick-thumb" autoplay>
                <div :style="{textAlign:'center'}"><img :src="imgpath.public.HomeImage1"></div>
                <div :style="{textAlign:'center'}"><img :src="imgpath.public.HomeImage2"></div>
                <div :style="{textAlign:'center'}"><img :src="imgpath.public.HomeImage3"></div>
            </a-carousel>
            <div style="font-size:45px; margin: 30px 30px 0 30px">
                <strong><span class="linear">半熟芝士</span>共享平台</strong>
            </div>
            <div style="font-size:15px; margin: 10px">
                半熟芝士，有识之士
            </div>
            <div v-if="!isLogin">
                <a-button @click="login" type="primary" size="large"
                          style="width: 150px; height: 45px;font-size: 20px; margin: 10px">
                    登录
                </a-button>
                <a-divider type="vertical"/>
                <a-button @click="register" size="large"
                          style="width: 150px; height: 45px;font-size: 20px; margin: 10px">
                    注册
                </a-button>
            </div>
            <div v-if="isLogin">
                <a-button @click="toCheckIn"
                          type="primary" size="large" style="width: 150px; height: 45px;font-size: 20px; margin: 10px">
                    进入选课
                </a-button>
            </div>
        </div>
    </div>
</template>
<script>

    export default {
        inject: ['login', 'register'],
        data() {
            return {
                isLogin: false,
                timer: '',
            }
        },
        methods: {
            isLoginWatcher() {
                this.isLogin = this.$store.state.currentUserID !== ""
            },
            toCheckIn() {
                this.$router.push('/checkinsystem')
            }
        },
        destroyed() {
            clearInterval(this.timer);
        },
        mounted() {
            let _this = this;
            // 实时获取登录态
            this.isLoginWatcher();
            clearInterval(this.timer);
            this.timer = window.setInterval(function () {
                _this.isLoginWatcher();
            }, 100);
        },
        computed: {
            imgpath() {
                return this.$store.state.imageStyle;
            },
            currentUserID() {
                return this.$store.state.currentUserID;
            },
        }
    }
</script>
<style scoped>
   .linear {
        background-image: -webkit-linear-gradient(right, #00B2FF, #007AFF); /* Safari 5.1 - 6.0 */
        background-image: -o-linear-gradient(right, #00B2FF, #007AFF); /* Opera 11.1 - 12.0 */
        background-image: -moz-linear-gradient(right, #00B2FF, #007AFF); /* Firefox 3.6 - 15 */
        background-image: linear-gradient(right, #00B2FF, #007AFF); /* 标准的语法 */
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        -webkit-animation: hue 6s infinite linear;
    }
    .ant-carousel >>> .slick-dots {
        height: auto
    }

    .ant-carousel >>> .slick-slide img {
        border: 5px solid #FFF;
        display: block;
        margin: auto;
        max-width: 80%;
    }

    .ant-carousel >>> .slick-thumb {
        bottom: -45px;
    }

    .ant-carousel >>> .slick-thumb li {
        width: 60px;
        height: 45px;
    }

    .ant-carousel >>> .slick-thumb li img {
        width: 100%;
        height: 100%;
        filter: grayscale(100%);
    }

    .ant-carousel >>> .slick-thumb li.slick-active img {
        filter: grayscale(0%);
    }
</style>
