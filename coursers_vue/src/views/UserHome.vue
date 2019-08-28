<template>
    <div class="home">
        <a-breadcrumb style="margin: 16px 0">
            <a-breadcrumb-item>个人中心</a-breadcrumb-item>
        </a-breadcrumb>
        <div :style="{ padding: '24px', background: '#fff', minHeight: '450px' }">
            <a-card title="个人信息">
                <a href="#" slot="extra" @click="edit = true">编辑信息</a>
                <a-form :form="editForm" prop="editForm" layout="horizontal" @submit="doEdit">
                    <a-form-item label="用户名" :label-col="formItemLayout.labelCol"
                                 :wrapper-col="formItemLayout.wrapperCol">
                        <a-input :disabled="!edit" v-decorator="['userName',
                                            {
                                                rules: [ {
                                                  required: true, message: '请输入用户名',
                                                }]
                                          }
                                        ]"/>
                    </a-form-item>
                    <a-form-item :label="currentUserType === '0' ? '学号' : '教工号'"
                                 :label-col="formItemLayout.labelCol"
                                 :wrapper-col="formItemLayout.wrapperCol">
                        <a-input :disabled="!edit" v-decorator="['userIDCard',
                                            {
                                                rules: [ {
                                                  required: true, message: currentUserType === '0' ? '请输入学号' : '请输入教工号',
                                                }]
                                          }
                                        ]"/>
                    </a-form-item>
                    <a-form-item label="电子邮箱" :label-col="formItemLayout.labelCol"
                                 :wrapper-col="formItemLayout.wrapperCol">
                        <a-input :disabled="!edit" v-decorator="['email',
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
                        <a-input :disabled="!edit" v-decorator="['phoneNum',
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
                        <a-input :disabled="!edit" v-decorator="['school',
                                            {
                                                rules: [ {
                                                  required: true, message: '请输入学校',
                                                }]
                                          }
                                        ]"/>
                    </a-form-item>
                    <a-form-item label="学院" :label-col="formItemLayout.labelCol"
                                 :wrapper-col="formItemLayout.wrapperCol">
                        <a-input :disabled="!edit" v-decorator="['college',
                                            {
                                                rules: [ {
                                                  required: true, message: '请输入学院',
                                                }]
                                          }
                                        ]"/>
                    </a-form-item>
                    <a-form-item v-show="currentUserType === '0'" label="班级"
                                 :label-col="formItemLayout.labelCol"
                                 :wrapper-col="formItemLayout.wrapperCol">
                        <a-input :disabled="!edit" v-decorator="['subordinateClass']"/>
                    </a-form-item>
                    <a-divider></a-divider>
                    <a-row>
                        <a-col :span="24" :style="{ textAlign: 'right' }">
                            <a-button :disabled="!edit" @click="edit=false">
                                关闭
                            </a-button>
                            <a-divider type="vertical"></a-divider>
                            <a-button :disabled="!edit" type="primary" html-type="submit">
                                保存
                            </a-button>
                        </a-col>
                    </a-row>
                </a-form>
            </a-card>
            <a-card title="选课记录" style="margin-top: 20px">
                <a-table bordered :dataSource="checkInLog" :columns="columns" rowKey="pk" :pagination="false">
                    <template slot="operation" slot-scope="text, record">
                        <a-popconfirm
                                v-if="checkInLog.length"
                                title="确定要删除这条记录吗？"
                                @confirm="() => onDelete(record.pk)">
                            <a href="javascript:;">删除</a>
                        </a-popconfirm>
                    </template>
                </a-table>
                <a-row :gutter="24" type="flex" justify="end" style="margin-top: 12px">
                    <a-pagination showSizeChanger showQuickJumper :pageSize.sync="pageSize"
                                  @showSizeChange="onShowSizeChange" @change="onPageNumChange" :total="total"
                                  v-model="current" :showTotal="total => `共 ${total} 条记录`"/>
                </a-row>
            </a-card>
        </div>

    </div>
</template>

<script>
    import axios from 'axios'
    import {SelectionLog, User} from "../assets/js/url";

    export default {
        beforeCreate() {
            this.editForm = this.$form.createForm(this);
        },
        data() {
            return {
                checkInLog: [],
                userInfo: [],
                edit: false,
                columns: [{
                    title: '用户名',
                    dataIndex: 'user_Name',
                    width: '30%',
                }, {
                    title: '课程名',
                    dataIndex: 'selectedCourse_Name',
                }, {
                    title: '选课时间',
                    dataIndex: 'time',
                }, {
                    title: '操作',
                    dataIndex: 'operation',
                    scopedSlots: {customRender: 'operation'},
                }],
                pageSize: 10,
                current: 1,
                total: 0,
                visible: false,
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
            };
        },
        mounted() {
            this.getUserInfo();
            this.getSelectionLogList();
        },
        methods: {
            convertUTCDateToLocalDate(date) {
                let localTime = date;
                localTime = localTime.substr(0, date.lastIndexOf('.'));
                localTime = localTime.replace('T', ' ');
                return localTime;
            },
            onShowSizeChange(current, pageSize) {
                this.current = 1;
                this.getSelectionLogList()
            },
            onPageNumChange(pageNumber) {
                this.current = pageNumber;
                this.getSelectionLogList()
            },
            getSelectionLogList() {
                let that = this;
                axios.get(SelectionLog, {
                    params: {
                        size: this.pageSize,
                        page: this.current
                    }
                }).then(
                    res => {
                        if (res.status === 200) {
                            that.total = res.data.count;
                            that.checkInLog = res.data.results;
                            for (let log of that.checkInLog) {
                                log.time = this.convertUTCDateToLocalDate(log.time);
                            }
                        }
                    })
                    .catch(
                        err => {
                            that.$message.info(err.response.data.detail);
                        }
                    )
            },
            onDelete(key) {
                let formData = new FormData();
                formData.append('valid', '0');
                axios.patch(SelectionLog + '/' + key, formData)
                    .then(
                        res => {
                            if (res.status === 200) {
                                this.$message.info("删除成功");
                                this.current = 1;
                                this.getSelectionLogList();
                            }
                        }
                    ).catch(
                    err => {
                        this.$message.error(item + ' ' + err.response.data.detail);
                    }
                )
            },
            getUserInfo() {
                axios.get(User + '/' + this.currentUserID).then(
                    res => {
                        if (res.status === 200) {
                            this.userInfo = res.data;
                            this.editForm.setFieldsValue({
                                'userName': this.userInfo.userName,
                                'userIDCard': this.userInfo.userIDCard,
                                'email': this.userInfo.email,
                                'school': this.userInfo.school,
                                'phoneNum': this.userInfo.phoneNum,
                                'college': this.userInfo.college,
                                'subordinateClass': this.userInfo.subordinateClass
                            })
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
            doEdit(e) {
                e.preventDefault();
                let that = this;
                this.editForm.validateFields((err, values) => {
                    if (!err) {
                        let formData = new FormData();
                        formData.append('userName', values.userName);
                        formData.append('userIDCard', values.userIDCard);
                        formData.append('email', values.email);
                        formData.append('phoneNum', values.phoneNum);
                        formData.append('school', values.school);
                        formData.append('college', values.college);
                        if (that.currentUserType === '0') {
                            formData.append('subordinateClass', values.subordinateClass);
                        }
                        axios.patch(User + '/' + that.currentUserID, formData).then(
                            res => {
                                if (res.status === 200) {
                                    that.$message.info("保存成功");
                                    that.getUserInfo();
                                    that.edit = false
                                }
                            }
                        ).catch(
                            err => {
                                for (let item in err.response.data) {
                                    that.$message.error(item + ' ' + err.response.data[item]);
                                }
                            }
                        )
                    }
                });
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
    };
</script>
