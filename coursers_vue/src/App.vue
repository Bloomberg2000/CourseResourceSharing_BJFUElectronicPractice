<template>
    <a-locale-provider :locale="zhCN">
        <a-layout id="app" style="min-height: 100vh">
            <a-layout-header>
                <div class="logo">
                    <img style="height: 32px" :src="imgpath.public.logo"/>
                    <span class="logoText">
                    半熟芝士共享平台
                </span>
                </div>
                <a-menu theme="dark" mode="horizontal" @click="NavClick" :defaultSelectedKeys="['home']"
                        :style="{ lineHeight: '64px' }">
                    <a-menu-item key="home">
                        <a-icon type="home"/>
                        <span>首页</span>
                    </a-menu-item>
                    <a-menu-item key="checkinsystem">
                        <a-icon type="schedule"/>
                        <span>选课系统</span>
                    </a-menu-item>
                    <a-menu-item key="friendlylink">
                        <a-icon type="team"/>
                        <span>友情链接</span>
                    </a-menu-item>
                    <a-menu-item v-if="!isLogin" key="login" class="nav-right">
                        <a-icon type="login"/>
                        登录
                    </a-menu-item>
                    <a-menu-item v-if="!isLogin" key="register" class="nav-right">
                        <a-icon type="user-add"/>
                        注册
                    </a-menu-item>
                    <a-menu-item v-if="isLogin" key="logout" class="nav-right">
                        <a-icon type="logout"/>
                        注销
                    </a-menu-item>
                    <a-sub-menu v-if="isLogin" key="sub1" class="nav-right">
                        <span slot="title"><a-icon type="user"/><span>{{userInfo.userName}}</span></span>
                        <a-menu-item key="userhome">我的信息</a-menu-item>
                        <a-menu-item v-if="this.currentUserType === '1'" key="admin">后台管理</a-menu-item>
                    </a-sub-menu>
                </a-menu>
            </a-layout-header>
            <a-layout-content style="padding: 0 50px">
                <router-view/>
            </a-layout-content>
            <a-layout-footer style="text-align: center">
                课程共享平台 © 半熟芝士团队TM 2019
            </a-layout-footer>
            <a-modal title="登录" :visible="LoginModalShow" footer @cancel="closeModal">
                <a-form id="components-form-demo-normal-login" :form="LoginForm" prop="LoginForm" class="login-form"
                        @submit="doLogin">
                    <a-form-item>
                        <a-input v-decorator="['userName',{ rules: [{ required: true, message: '用户名不能为空' }] }]"
                                 placeholder="请输入用户名/邮箱/手机号">
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
                <a-form :form="RegisterForm" prop="RegisterForm" layout="horizontal" @submit="doRegister">
                    <a-form-item label="类别" :label-col="formItemLayout.labelCol"
                                 :wrapper-col="formItemLayout.wrapperCol">
                        <a-radio-group v-decorator="['type',
                                            {
                                                rules: [ {
                                                  required: true, message: '请选择类别',
                                                }]
                                          }
                                        ]">
                            <a-radio-button value="0">学生</a-radio-button>
                            <a-radio-button value="1">教师</a-radio-button>
                        </a-radio-group>
                    </a-form-item>
                    <a-form-item label="用户名" :label-col="formItemLayout.labelCol"
                                 :wrapper-col="formItemLayout.wrapperCol">
                        <a-input v-decorator="['userName',
                                            {
                                                rules: [ {
                                                  required: true, message: '请输入用户名',
                                                }]
                                          }
                                        ]"/>
                    </a-form-item>
                    <a-form-item :label="this.RegisterForm.getFieldValue('type') === '0' ? '学号' : '教工号'"
                                 :label-col="formItemLayout.labelCol"
                                 :wrapper-col="formItemLayout.wrapperCol">
                        <a-input v-decorator="['userIDCard',
                                            {
                                                rules: [ {
                                                  required: true, message: this.RegisterForm.getFieldValue('type') === '0' ? '请输入学号' : '请输入教工号',
                                                }]
                                          }
                                        ]"/>
                    </a-form-item>
                    <a-form-item label="电子邮箱" :label-col="formItemLayout.labelCol"
                                 :wrapper-col="formItemLayout.wrapperCol">
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
                    <a-form-item label="手机号码" :label-col="formItemLayout.labelCol"
                                 :wrapper-col="formItemLayout.wrapperCol">
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
                    <a-form-item label="学校" :label-col="formItemLayout.labelCol"
                                 :wrapper-col="formItemLayout.wrapperCol">
                        <a-input v-decorator="['school',
                                            {
                                                rules: [ {
                                                  required: true, message: '请输入学校',
                                                }]
                                          }
                                        ]"/>
                    </a-form-item>
                    <a-form-item label="学院" :label-col="formItemLayout.labelCol"
                                 :wrapper-col="formItemLayout.wrapperCol">
                        <a-input v-decorator="['college',
                                            {
                                                rules: [ {
                                                  required: true, message: '请输入学院',
                                                }]
                                          }
                                        ]"/>
                    </a-form-item>
                    <a-form-item v-show="this.RegisterForm.getFieldValue('type') === '0'" label="班级"
                                 :label-col="formItemLayout.labelCol"
                                 :wrapper-col="formItemLayout.wrapperCol">
                        <a-input v-decorator="['subordinateClass']"/>
                    </a-form-item>
                    <a-form-item label="密码" :label-col="formItemLayout.labelCol"
                                 :wrapper-col="formItemLayout.wrapperCol">
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
    </a-locale-provider>
</template>
<script>
    import zhCN from 'ant-design-vue/lib/locale-provider/zh_CN';
    import axios from 'axios'
    import {Auth, User} from "./assets/js/url";

    export default {
        provide() {
            return {
                login: this.login,
                register: this.register
            }
        },
        beforeCreate() {
            this.LoginForm = this.$form.createForm(this, {prop: 'LoginForm'});
            this.RegisterForm = this.$form.createForm(this, {prop: 'RegisterForm'});
        },
        data() {
            return {
                zhCN,
                confirmDirty: false,
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
                        that.$store.commit("userChange", '');
                        this.$store.commit("userTypeChange", '0');
                        this.$Message.info(err.response.data.message);
                    }
                )
            },
            doLogin(e) {
                e.preventDefault();
                this.LoginForm.validateFields((err, values) => {
                    if (!err) {
                        let formData = new FormData();
                        formData.append('userName', values.userName);
                        formData.append('password', values.password);
                        axios.post(Auth, formData).then(
                            res => {
                                if (res.status === 202) {
                                    this.$message.info("登录成功");
                                    this.$store.commit("userChange", res.data.userID[0] + '');
                                    this.$store.commit("userTypeChange", res.data.userType[0] + '');
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
                        formData.append('type', values.type);
                        formData.append('userName', values.userName);
                        formData.append('userIDCard', values.userIDCard);
                        formData.append('email', values.email);
                        formData.append('phoneNum', values.phoneNum);
                        formData.append('password', values.password);
                        formData.append('school', values.school);
                        formData.append('college', values.college);
                        if (values.type === '0') {
                            formData.append('subordinateClass', values.subordinateClass);
                        }
                        axios.post(User, formData).then(
                            res => {
                                if (res.status === 201) {
                                    this.$message.info("注册成功");
                                    this.closeModal();
                                    this.RegisterForm.resetFields()
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
            login() {
                this.LoginModalShow = true;
            },
            register() {
                this.RegisterModalShow = true;
            },
            NavClick(item) {
                if (item.key === 'home') {
                    this.$router.push('/');
                }
                if (item.key === 'checkinsystem') {
                    this.$router.push('/checkinsystem');
                }
                if (item.key === 'friendlylink') {
                    this.$router.push('/friendlylink');
                }
                if (item.key === 'userhome') {
                    this.$router.push('/userhome');
                }
                if (item.key === 'admin') {
                    this.$router.push('admin');
                }
                if (item.key === 'login') {
                    this.login();
                }
                if (item.key === 'register') {
                    this.register();
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
                                        this.$store.commit("userTypeChange", '0');
                                        that.userInfo = [];
                                        that.isLoginWatcher();
                                        that.$message.info("注销成功");
                                        this.$router.push('/')
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
            currentUserType() {
                return this.$store.state.currentUserType;
            },
        }
    }
</script>

<style>
    #app .logo {
        /*width: 200px;*/
        height: 31px;
        float: left;
    }

    #app .logo .logoText {
        font-size: 15px;
        color: #ffffff;
        padding: 10px;
    }

    .nav-right {
        float: right;
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
