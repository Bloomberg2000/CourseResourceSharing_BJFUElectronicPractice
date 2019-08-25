<template>
    <a-layout id="app" style="min-height: 100vh">
        <a-layout-sider collapsible v-model="collapsed">
            <div class="logo">
                <img style="height: 32px" :src="imgpath.public.logo"/>
                <span class="logoText" v-show="!collapsed">课程共享平台</span>
            </div>
            <a-menu theme="dark" @click="NavClick" :defaultSelectedKeys="['1']" mode="inline">
                <a-menu-item key="home">
                    <a-icon type="schedule"/>
                    <span>选课系统</span>
                </a-menu-item>
                <a-menu-item key="friendlylink">
                    <a-icon type="team"/>
                    <span>友情链接</span>
                </a-menu-item>
                <a-sub-menu key="sub1">
                    <span slot="title"><a-icon type="user"/><span>个人中心</span></span>
                    <a-menu-item key="userhome">我的信息</a-menu-item>
                    <a-menu-item key="checkinlog">选课记录</a-menu-item>
                </a-sub-menu>
            </a-menu>
        </a-layout-sider>
        <a-layout>
            <a-menu mode="horizontal" @click="topNavClick" :style="{ textAlign: 'right' }">
                <a-menu-item v-show="!isLogin" key="login">
                    <a-icon type="login"/>
                    登录
                </a-menu-item>
                <a-menu-item v-show="!isLogin" key="register">
                    <a-icon type="user-add"/>
                    注册
                </a-menu-item>
                <a-menu-item v-if="isLogin" key="userName">
                    <a-icon type="user"/>
                    {{userInfo.userName}}
                </a-menu-item>
                <a-menu-item v-show="isLogin" key="logout">
                    <a-icon type="logout"/>
                    注销
                </a-menu-item>
            </a-menu>
            <!--            </a-layout-header>-->
            <a-layout-content style="margin: 0 16px">
                <router-view/>
            </a-layout-content>
            <a-layout-footer style="text-align: center">
                课程共享平台 ©2018
            </a-layout-footer>
        </a-layout>
        <a-modal title="登录" :visible="LoginModalShow" footer @cancel="closeModal">
            <a-form id="components-form-demo-normal-login" :form="LoginForm" prop="LoginForm" class="login-form"
                    @submit="doLogin">
                <a-form-item>
                    <a-input v-decorator="['userName',{ rules: [{ required: true, message: '用户名不能为空' }] }]"
                             placeholder="请输入用户名/邮箱/手机号/学号">
                        <a-icon slot="prefix" type="user" style="color: rgba(0,0,0,.25)"/>
                    </a-input>
                </a-form-item>
                <a-form-item>
                    <a-input v-decorator="['password',{ rules: [{ required: true, message: '密码不能为空' }] }]"
                             type="password" placeholder="密码">
                        <a-icon slot="prefix" type="lock" style="color: rgba(0,0,0,.25)"/>
                    </a-input>
                </a-form-item>
                <a-form-item>
                    <a-button type="primary" html-type="submit" class="login-form-button">
                        登录
                    </a-button>
                    或者 <a>现在注册</a>
                    <a class="login-form-forgot">忘记密码</a>
                </a-form-item>
            </a-form>
        </a-modal>
        <a-modal title="注册" :visible="RegisterModalShow" @cancel="closeModal">
            <template slot="footer">
                <a-button key="back" @click="closeModal">取消</a-button>
                <a-button key="submit" type="primary" @click="doRegister">注册</a-button>
            </template>
            <a-form :form="RegisterForm" prop="RegisterForm" layout="horizontal" @submit="doLogin">
                <a-form-item label="用户名" :label-col="formItemLayout.labelCol" :wrapper-col="formItemLayout.wrapperCol">
                    <a-input v-decorator="['userName',
                                            {
                                                rules: [ {
                                                  required: true, message: '请输入用户名',
                                                }]
                                          }
                                        ]"/>
                </a-form-item>
                <a-form-item label="学号" :label-col="formItemLayout.labelCol" :wrapper-col="formItemLayout.wrapperCol">
                    <a-input v-decorator="['stuCode',
                                            {
                                                rules: [ {
                                                  required: true, message: '请输入学号',
                                                }]
                                          }
                                        ]"/>
                </a-form-item>
                <a-form-item label="电子邮箱" :label-col="formItemLayout.labelCol" :wrapper-col="formItemLayout.wrapperCol">
                    <a-input v-decorator="['email',
                                            {
                                                rules: [{
                                                  type: 'email', message: '电子邮箱格式不正确',
                                                }, {
                                                  required: true, message: '请输入电子邮箱',
                                                }]
                                          }
                                        ]"/>
                </a-form-item>
                <a-form-item label="手机号码" :label-col="formItemLayout.labelCol" :wrapper-col="formItemLayout.wrapperCol">
                    <a-input v-decorator="['phoneNum',
                                          {
                                            rules: [{
                                                required: true, message: '请输入手机号码'
                                             },{
                                                pattern: /^1[3456789]\d{9}$/, message: '手机号码格式不正确'
                                             }],
                                          }
                                        ]" style="width: 100%"
                    >
                        <a-select slot="addonBefore" v-decorator="['prefix',{ initialValue: '86' }]"
                                  style="width: 70px">
                            <a-select-option value="86">
                                +86
                            </a-select-option>
                        </a-select>
                    </a-input>
                </a-form-item>
                <a-form-item label="学校" :label-col="formItemLayout.labelCol" :wrapper-col="formItemLayout.wrapperCol">
                    <a-input v-decorator="['school',
                                            {
                                                rules: [ {
                                                  required: true, message: '请输入学校',
                                                }]
                                          }
                                        ]"/>
                </a-form-item>
                <a-form-item label="学院" :label-col="formItemLayout.labelCol" :wrapper-col="formItemLayout.wrapperCol">
                    <a-input v-decorator="['college',
                                            {
                                                rules: [ {
                                                  required: true, message: '请输入学院',
                                                }]
                                          }
                                        ]"/>
                </a-form-item>
                <a-form-item label="班级" :label-col="formItemLayout.labelCol" :wrapper-col="formItemLayout.wrapperCol">
                    <a-input v-decorator="['subordinateClass',
                                            {
                                                rules: [ {
                                                  required: true, message: '请输入班级',
                                                }]
                                          }
                                        ]"/>
                </a-form-item>
                <a-form-item label="密码" :label-col="formItemLayout.labelCol" :wrapper-col="formItemLayout.wrapperCol">
                    <a-input v-decorator="['password',
                                            {
                                                rules: [{
                                                  required: true, message: '请输入密码',
                                                }, {
                                                  validator: validateToNextPassword,
                                                }],
                                              }
                                            ]"
                             type="password"/>
                </a-form-item>
                <a-form-item label="再次输入密码" :label-col="formItemLayout.labelCol"
                             :wrapper-col="formItemLayout.wrapperCol">
                    <a-input v-decorator="['confirm',
                                              {
                                                rules: [{
                                                  required: true, message: '请再次输入密码',
                                                }, {
                                                  validator: compareToFirstPassword,
                                                }],
                                              }
                                            ]"
                             type="password"
                             @blur="handleConfirmBlur"/>
                </a-form-item>
            </a-form>
        </a-modal>
    </a-layout>
</template>
<script>
    import axios from 'axios'
    import {Auth, User} from "./assets/js/url";

    export default {
        beforeCreate() {
            this.LoginForm = this.$form.createForm(this, {prop: 'LoginForm'});
            this.RegisterForm = this.$form.createForm(this, {prop: 'RegisterForm'});
        },
        data() {
            return {
                confirmDirty: false,
                collapsed: true,
                LoginModalShow: false,
                RegisterModalShow: false,
                timer: '',
                isLogin: false,
                userInfo: '',
                formItemLayout: {
                    labelCol: {
                        xs: {span: 24},
                        sm: {span: 6},
                    },
                    wrapperCol: {
                        xs: {span: 24},
                        sm: {span: 14},
                    },
                },
            }
        },
        methods: {
            getUserInfo() {
                axios.get(User + '/' + this.currentUserID).then(
                    res => {
                        if (res.status === 200) {
                            this.userInfo = res.data;
                        }
                    }
                ).catch(
                    err => {
                        this.$store.commit("userChange", '');
                        this.$Message.info(err.response.data.message);
                    }
                )
            },
            doLogin(e) {
                e.preventDefault();
                this.LoginForm.validateFields((err, values) => {
                    if (!err) {
                        console.log('Received values of form: ', values);
                        let formData = new FormData();
                        formData.append('userName', values.userName);
                        formData.append('password', values.password);
                        axios.post(Auth, formData).then(
                            res => {
                                if (res.status === 202) {
                                    this.$message.info("登录成功");
                                    this.$store.commit("userChange", res.data.userID[0] + '');
                                    this.closeModal();
                                }
                            }
                        ).catch(
                            err => {
                                this.$message.error(err.response.data.detail);
                            }
                        )
                    }
                });
            },
            doRegister(e) {
                e.preventDefault();
                this.RegisterForm.validateFields((err, values) => {
                    if (!err) {
                        let formData = new FormData();
                        formData.append('userName', values.userName);
                        formData.append('stuCode', values.stuCode);
                        formData.append('email', values.email);
                        formData.append('phoneNum', values.phoneNum);
                        formData.append('password', values.password);
                        formData.append('school', values.school);
                        formData.append('college', values.college);
                        formData.append('subordinateClass', values.subordinateClass);
                        axios.post(User, formData).then(
                            res => {
                                if (res.status === 201) {
                                    this.$message.info("注册成功");
                                    this.closeModal();
                                }
                            }
                        ).catch(
                            err => {
                                for (let item in err.response.data) {
                                    this.$message.error(item + ' ' + err.response.data[item]);
                                }
                            }
                        )
                    }
                });
            },
            closeModal() {
                this.LoginModalShow = false;
                this.RegisterModalShow = false;
            },
            handleConfirmBlur(e) {
                const value = e.target.value;
                this.confirmDirty = this.confirmDirty || !!value;
            },
            compareToFirstPassword(rule, value, callback) {
                const form = this.RegisterForm;
                if (value && value !== form.getFieldValue('password')) {
                    callback('两次输入的密码不一致');
                } else {
                    callback();
                }
            },
            validateToNextPassword(rule, value, callback) {
                const form = this.RegisterForm;
                if (value && this.confirmDirty) {
                    form.validateFields(['confirm'], {force: true});
                }
                callback();
            },
            NavClick(item) {
                if (item.key === 'home') {
                    this.$router.push('/');
                }
                if (item.key === 'friendlylink') {
                    this.$router.push('/friendlylink');
                }
                if (item.key === 'userhome') {
                    this.$router.push('/userhome');
                }
                if (item.key === 'checkinlog') {
                    this.$router.push('checkinlog');
                }
            },
            topNavClick(item) {
                if (item.key === 'login') {
                    this.LoginModalShow = true;
                }
                if (item.key === 'register') {
                    this.RegisterModalShow = true;
                }
                if (item.key === 'logout') {
                    let that = this;
                    this.$confirm({
                        title: '注销',
                        content: '确定要注销当前账户吗',
                        cancelText: '取消',
                        okText: '确定',
                        onOk: () => {
                            axios.get(Auth).then(
                                res => {
                                    if (res.status === 200) {
                                        that.$store.commit("userChange", '');
                                        that.userInfo = [];
                                        that.isLoginWatcher();
                                        that.$message.info("注销成功");
                                    }
                                }
                            ).catch(
                                err => {
                                    that.$message.info(err.response.data.detail);
                                }
                            )
                        }
                    })
                }
            },
            isLoginWatcher() {
                this.isLogin = this.$store.state.currentUserID !== ""
            },
        },
        destroyed() {
            clearInterval(this.timer);
        },
        watch: {
            currentUserID(userID) {
                // 用户ID变化重新获取用户信息
                if (userID !== "") {
                    this.getUserInfo();
                }
            },
        },
        mounted() {
            let _this = this;
            // 实时获取登录态
            this.isLoginWatcher();
            clearInterval(this.timer);
            this.timer = window.setInterval(function () {
                _this.isLoginWatcher();
            }, 100);
            // 每次打开页面重新获取用户信息
            let userID = this.$store.state.currentUserID;
            if (userID !== '') {
                this.getUserInfo();
            }
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

    #components-form-demo-normal-login .login-form {
        max-width: 300px;
    }

    #components-form-demo-normal-login .login-form-forgot {
        float: right;
    }

    #components-form-demo-normal-login .login-form-button {
        width: 100%;
    }
</style>
