<template>
    <div class="home">
        <a-breadcrumb style="margin: 16px 0">
            <a-breadcrumb-item>选课系统</a-breadcrumb-item>
        </a-breadcrumb>
        <div :style="{ padding: '24px', background: '#fff', minHeight: '450px' }">
            <a-form class="ant-advanced-search-form" :form="form" @submit="handleSearch" :style="{padding: '24px'}"
                    v-bind="formItemLayout">
                <div :style="{marginBottom:'10px'}">筛选课程</div>
                <a-row :gutter="24">
                    <a-col v-bind="formLayout">
                        <a-form-item label="课程名称">
                            <a-input placeholder="请输入课程名称"/>
                        </a-form-item>
                    </a-col>
                    <a-col v-bind="formLayout">
                        <a-form-item label="所属学校">
                            <a-input placeholder="请输入所属学校/学院"/>
                        </a-form-item>
                    </a-col>
                    <a-col v-bind="formLayout">
                        <a-form-item label="课程学时">
                            <a-input placeholder="请输入学时"/>
                        </a-form-item>
                    </a-col>
                    <a-col v-bind="formLayout">
                        <a-form-item label="开课时间">
                            <a-range-picker v="12"/>
                        </a-form-item>
                    </a-col>
                </a-row>
                <a-row>
                    <a-col :span="24" :style="{ textAlign: 'right' }">
                        <a-button type="primary" html-type="submit">
                            搜索
                        </a-button>
                        <a-button :style="{ marginLeft: '8px' }" @click="handleReset">
                            清除
                        </a-button>
                    </a-col>
                </a-row>
            </a-form>
            <a-row :gutter="24">
                <a-col v-bind="courseCardLayout" v-for="(item,index) in courseList" v-key="item">
                    <a-card hoverable style="margin-top:10px ">
                        <template class="ant-card-actions" slot="actions">
                            <a-tooltip placement="top">
                                <template slot="title">
                                    <span>收藏（暂未开放）</span>
                                </template>
                                <a-icon type="star"/>
                            </a-tooltip>
                            <a-tooltip placement="top">
                                <template slot="title">
                                    <span>评论（暂未开放）</span>
                                </template>
                                <a-icon type="message"/>
                            </a-tooltip>
                            <a-tooltip placement="top">
                                <template slot="title">
                                    <span>我要选课</span>
                                </template>
                                <a-icon type="link"/>
                            </a-tooltip>
                            <a-tooltip placement="top">
                                <template slot="title">
                                    <span>查看详情</span>
                                </template>
                                <a-icon type="ellipsis"/>
                            </a-tooltip>
                        </template>
                        <a-card-meta
                                :title="item.name"
                                :description="item.info">
                            <!--                    <a-avatar slot="avatar" src="https://zos.alipayobjects.com/rmsportal/ODTLcjxAfvqbxHnVXCYX.png"/>-->
                        </a-card-meta>
                    </a-card>
                </a-col>
            </a-row>
        </div>

    </div>
</template>

<script>
    import axios from 'axios'
    import {Course} from "../assets/js/url";

    export default {
        data() {
            return {
                expand: false,
                form: this.$form.createForm(this),
                formLayout: {
                    lg: {span: 12},
                    md: {span: 24},
                },
                courseList: [],
                courseCardLayout: {
                    lg: {span: 12},
                    md: {span: 24}
                },
            };
        },
        mounted() {
            this.getCourseList();
        },
        methods: {
            handleSearch(e) {
                e.preventDefault();
                this.form.validateFields((error, values) => {
                });
            },
            handleReset() {
                this.form.resetFields();
            },
            getCourseList() {
                let that = this;
                axios.get(Course)
                    .then(
                        res => {
                            if (res.status === 200) {
                                that.courseList = res.data;
                            }
                        })
                    .catch(
                        err => {
                            that.$message.info(err.response.data.detail);
                        }
                    )
            }
        },
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
</style>
