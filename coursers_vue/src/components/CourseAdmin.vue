<template>
    <div class="checkinsystem">
        <a-form layout="inline" :form="form" ref="form" @submit="handleSearch" :style="{padding: '24px'}">
            <a-form-item label="课程名称">
                <a-input placeholder="请输入课程名称" v-decorator="['name']"/>
            </a-form-item>
            <a-form-item label="所属学校">
                <a-input placeholder="请输入所属学校" v-decorator="['subordinateSchoolAndCollege']"/>
            </a-form-item>
            <a-form-item label="模糊搜索">
                <a-input placeholder="请输入要搜索的内容" v-decorator="['info']"/>
            </a-form-item>
            <a-form-item>
                <a-button type="primary" html-type="submit">
                    搜索
                </a-button>
                <a-divider type="vertical"/>
                <a-button :style="{ marginLeft: '8px' }" @click="handleReset">
                    清除
                </a-button>
            </a-form-item>
            <a-form-item style="float: right">
                <a-button @click="AddCourseModal = true">
                    添加
                </a-button>
            </a-form-item>
        </a-form>
        <a-table :columns="columns" :dataSource="courseList" :pagination="false" rowKey="pk">
            <template slot="action" slot-scope="text, record">
                <a @click="beforeEdit(record)">编辑</a>
                <a-divider type="vertical"/>
                <a-popconfirm
                        v-if="courseList.length"
                        title="确定要删除这条记录吗？"
                        @confirm="() => doDelete(record.pk)">
                    <a>删除</a>
                </a-popconfirm>
            </template>
        </a-table>
        <a-row :gutter="24" type="flex" justify="end" style="margin-top: 12px">
            <a-pagination showSizeChanger showQuickJumper :pageSize.sync="pageSize"
                          @showSizeChange="onShowSizeChange" @change="onPageNumChange" :total="total"
                          v-model="current" :showTotal="total => `共 ${total} 条记录`"/>
        </a-row>
        <a-modal title="添加课程" :visible="AddCourseModal" @cancel="closeModal">
            <template slot="footer">
                <a-button key="back" @click="closeModal">取消</a-button>
                <a-button key="submit" type="primary" @click="doAdd">添加</a-button>
            </template>
            <a-form :form="AddForm" prop="AddForm" layout="horizontal" @submit="doAdd">
                <a-form-item label="课程名称" :label-col="formItemLayout.labelCol"
                             :wrapper-col="formItemLayout.wrapperCol">
                    <a-input v-decorator="['name',
                                            {
                                                rules: [ {
                                                  required: true, message: '请输入课程名称',
                                                }]
                                          }
                                        ]"/>
                </a-form-item>
                <a-form-item label="所属学校" :label-col="formItemLayout.labelCol"
                             :wrapper-col="formItemLayout.wrapperCol">
                    <a-input v-decorator="['subordinateSchoolAndCollege',
                                            {
                                                rules: [ {
                                                  required: true, message: '请输入所属学校',
                                                }]
                                          }
                                        ]"/>
                </a-form-item>
                <a-form-item label="选课人数" :label-col="formItemLayout.labelCol"
                             :wrapper-col="formItemLayout.wrapperCol">
                    <a-input v-decorator="['checkInNum',
                                            {
                                                rules: [ {
                                                  required: true, message: '请输入选课人数',
                                                }]
                                          }
                                        ]"/>
                </a-form-item>
                <a-form-item label="课程详情" :label-col="formItemLayout.labelCol"
                             :wrapper-col="formItemLayout.wrapperCol">
                    <a-textarea autosize v-decorator="['info',
                                            {
                                                rules: [ {
                                                  required: true, message: '请输入课程详情',
                                                }]
                                          }
                                        ]"/>
                </a-form-item>
                <a-form-item label="课程链接" :label-col="formItemLayout.labelCol"
                             :wrapper-col="formItemLayout.wrapperCol">
                    <a-input v-decorator="['link',
                                            {
                                                rules: [ {
                                                  required: true, message: '请输入课程链接',
                                                }]
                                          }
                                        ]"/>
                </a-form-item>
                <a-form-item label="课程状态" :label-col="formItemLayout.labelCol"
                             :wrapper-col="formItemLayout.wrapperCol">
                    <a-input v-decorator="['currentStatus',
                                            {
                                                rules: [ {
                                                  required: true, message: '请输入课程状态',
                                                }]
                                          }
                                        ]"/>
                </a-form-item>
            </a-form>
        </a-modal>
        <a-modal title="编辑课程" :visible="EditCourseModal" @cancel="closeModal">
            <template slot="footer">
                <a-button key="back" @click="closeModal">取消</a-button>
                <a-button key="submit" type="primary" @click="doEdit">保存</a-button>
            </template>
            <a-form :form="EditForm" prop="EditForm" layout="horizontal" @submit="doEdit">
                <a-form-item label="课程名称" :label-col="formItemLayout.labelCol"
                             :wrapper-col="formItemLayout.wrapperCol">
                    <a-input v-decorator="['name',
                                            {
                                                rules: [ {
                                                  required: true, message: '请输入课程名称',
                                                }]
                                          }
                                        ]"/>
                </a-form-item>
                <a-form-item label="所属学校" :label-col="formItemLayout.labelCol"
                             :wrapper-col="formItemLayout.wrapperCol">
                    <a-input v-decorator="['subordinateSchoolAndCollege',
                                            {
                                                rules: [ {
                                                  required: true, message: '请输入所属学校',
                                                }]
                                          }
                                        ]"/>
                </a-form-item>
                <a-form-item label="选课人数" :label-col="formItemLayout.labelCol"
                             :wrapper-col="formItemLayout.wrapperCol">
                    <a-input v-decorator="['checkInNum',
                                            {
                                                rules: [ {
                                                  required: true, message: '请输入选课人数',
                                                }]
                                          }
                                        ]"/>
                </a-form-item>
                <a-form-item label="课程详情" :label-col="formItemLayout.labelCol"
                             :wrapper-col="formItemLayout.wrapperCol">
                    <a-textarea autosize v-decorator="['info',
                                            {
                                                rules: [ {
                                                  required: true, message: '请输入课程详情',
                                                }]
                                          }
                                        ]"/>
                </a-form-item>
                <a-form-item label="课程链接" :label-col="formItemLayout.labelCol"
                             :wrapper-col="formItemLayout.wrapperCol">
                    <a-input v-decorator="['link',
                                            {
                                                rules: [ {
                                                  required: true, message: '请输入课程链接',
                                                }]
                                          }
                                        ]"/>
                </a-form-item>
                <a-form-item label="课程状态" :label-col="formItemLayout.labelCol"
                             :wrapper-col="formItemLayout.wrapperCol">
                    <a-input v-decorator="['currentStatus',
                                            {
                                                rules: [ {
                                                  required: true, message: '请输入课程状态',
                                                }]
                                          }
                                        ]"/>
                </a-form-item>
            </a-form>
        </a-modal>
    </div>
</template>

<script>
    import axios from 'axios'
    import {Course, SelectionLog} from "../assets/js/url";

    const columns = [{
        title: '课程名称',
        dataIndex: 'name',
        key: 'name',
    }, {
        title: '所属学校',
        dataIndex: 'subordinateSchoolAndCollege',
        key: 'subordinateSchoolAndCollege',
        width: '120px'
    }, {
        title: '选课人数',
        dataIndex: 'checkInNum',
        key: 'checkInNum',
    }, {
        title: '课程详情',
        dataIndex: 'info',
        key: 'indo',
    }, {
        title: '课程链接',
        dataIndex: 'link',
        key: 'link',
    }, {
        title: '课程状态',
        dataIndex: 'currentStatus',
        key: 'currentStatus',
        width: '120px'
    }, {
        title: '操作',
        key: 'action',
        scopedSlots: {customRender: 'action'},
        width: '120px'
    }];

    export default {
        beforeCreate() {
        },
        data() {
            return {
                columns,
                AddCourseModal: false,
                EditCourseModal: false,
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
                expand: false,
                form: this.$form.createForm(this, {prop: 'form'}),
                AddForm: this.$form.createForm(this, {prop: 'AddForm'}),
                EditForm: this.$form.createForm(this, {prop: 'EditForm'}),
                courseList: [],
                pageSize: 10,
                current: 1,
                total: 0,
                courseData: []
            };
        },
        mounted() {
            this.getCourseList();
        },
        methods: {
            handleSearch(e) {
                this.current = 1;
                e.preventDefault();
                this.form.validateFields((error, values) => {
                    this.getCourseList(values.name, values.subordinateSchoolAndCollege, values.info);
                });
            },
            handleReset() {
                this.current = 1;
                this.getCourseList();
                this.form.resetFields();
            },
            onShowSizeChange(current, pageSize) {
                this.current = 1;
                this.getCourseList()
            },
            onPageNumChange(pageNumber) {
                this.current = pageNumber;
                this.getCourseList()
            },
            getCourseList(name = '', subordinateSchoolAndCollege = '', info = '') {
                let that = this;
                axios.get(Course, {
                    params: {
                        name: name,
                        subordinateSchoolAndCollege: subordinateSchoolAndCollege,
                        info: info,
                        size: this.pageSize,
                        page: this.current
                    }
                }).then(
                    res => {
                        if (res.status === 200) {
                            that.total = res.data.count;
                            that.courseList = res.data.results;
                            for (let data of that.courseList) {
                                data.info = data.info.substring(0, 50) + '...';
                            }
                        }
                    })
                    .catch(
                        err => {
                            that.$message.info(err.response.data.detail);
                        }
                    )
            },
            beforeEdit(item) {
                this.EditCourseModal = true;
                this.courseData = item;
                this.$nextTick(() => {
                    this.EditForm.setFieldsValue({
                        'name': this.courseData.name,
                        'subordinateSchoolAndCollege': this.courseData.subordinateSchoolAndCollege,
                        'checkInNum': this.courseData.checkInNum,
                        'info': this.courseData.info,
                        'link': this.courseData.link,
                        'currentStatus': this.courseData.currentStatus
                    });
                });
            },
            closeModal() {
                this.AddCourseModal = false;
                this.EditCourseModal = false;
            },
            doDelete(item) {
                let that = this;
                axios.delete(Course + '/' + item).then(
                    res => {
                        if (res.status === 204) {
                            this.$message.info("删除成功");
                            this.current = Math.ceil((this.total - 1) / this.pageSize);
                            this.getCourseList();
                        }
                    }
                ).catch(
                    err => {
                        this.$message.error(item + ' ' + err.response.data.detail);
                    }
                )
            },
            doEdit(e) {
                e.preventDefault();
                this.EditForm.validateFields((err, values) => {
                    if (!err) {
                        let formData = new FormData();
                        formData.append('name', values.name);
                        formData.append('subordinateSchoolAndCollege', values.subordinateSchoolAndCollege);
                        formData.append('checkInNum', values.checkInNum);
                        formData.append('info', values.info);
                        formData.append('link', values.link);
                        formData.append('currentStatus', values.currentStatus);
                        axios.patch(Course + '/' + this.courseData.pk, formData).then(
                            res => {
                                console.log(res);
                                if (res.status === 200) {
                                    this.$message.info("保存成功");
                                    this.getCourseList();
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
            doAdd(e) {
                e.preventDefault();
                this.AddForm.validateFields((err, values) => {
                    if (!err) {
                        let formData = new FormData();
                        formData.append('name', values.name);
                        formData.append('subordinateSchoolAndCollege', values.subordinateSchoolAndCollege);
                        formData.append('checkInNum', values.checkInNum);
                        formData.append('info', values.info);
                        formData.append('link', values.link);
                        formData.append('currentStatus', values.currentStatus);
                        axios.post(Course, formData).then(
                            res => {
                                console.log(res);
                                if (res.status === 201) {
                                    this.$message.info("添加成功");
                                    this.form.resetFields();
                                    this.current = Math.ceil((this.total + 1) / this.pageSize);
                                    this.getCourseList();
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
    };
</script>
<style>
    .ant-advanced-search-form {
        padding: 24px;
        border: 1px solid #d9d9d9;
        border-radius: 6px;
    }

    .ant-advanced-search-form .ant-form-item {
        display: flex;
    }

    .ant-advanced-search-form .ant-form-item-control-wrapper {
        flex: 1;
    }

    #components-form-demo-advanced-search .ant-form {
        max-width: none;
    }

    #components-form-demo-advanced-search .search-result-list {
        margin-top: 16px;
        border: 1px dashed #e9e9e9;
        border-radius: 6px;
        background-color: #fafafa;
        min-height: 200px;
        text-align: center;
        padding-top: 80px;
    }

    .title {
        padding: 10px 10px 0 10px;
        text-overflow: ellipsis;
        overflow: hidden;
        white-space: nowrap;
        flex: 1;
        display: inline-block;
        font-size: 20px;
        color: rgba(0, 0, 0, 0.85);
        font-weight: 500;
    }

    .subtitle {
        padding: 0 12px 0 12px;
        zoom: 1;
        font-size: 14px;
        font-variant: tabular-nums;
        line-height: 1.5;
        color: rgba(0, 0, 0, 0.4);
    }

    .content {
        padding: 12px;
        zoom: 1;
        font-size: 14px;
        font-variant: tabular-nums;
        line-height: 1.5;
        color: rgba(0, 0, 0, 0.65);
    }

    .footer {
        padding: 0 12px 0 12px;
        zoom: 1;
        font-size: 14px;
        font-variant: tabular-nums;
        line-height: 1.5;
        color: rgba(0, 0, 0, 0.4);
    }

    .detail_modal .title {
        padding: 10px 10px 0 10px;
        text-overflow: ellipsis;
        overflow: hidden;
        white-space: nowrap;
        flex: 1;
        display: inline-block;
        font-size: 30px;
        color: rgba(0, 0, 0, 0.85);
        font-weight: 500;
    }

    .detail_modal .subtitle {
        padding: 0 12px 0 12px;
        zoom: 1;
        font-size: 14px;
        font-variant: tabular-nums;
        line-height: 1.5;
        color: rgba(0, 0, 0, 0.4);
    }

    .detail_modal .content {
        padding: 16px 12px 12px 12px;
        zoom: 1;
        font-size: 14px;
        line-height: 2;
        color: rgba(0, 0, 0, 0.65);
    }

    .detail_modal .footer {
        padding: 0 12px 0 12px;
        zoom: 1;
        font-size: 14px;
        font-variant: tabular-nums;
        line-height: 1.5;
        color: rgba(0, 0, 0, 0.4);
    }
</style>
