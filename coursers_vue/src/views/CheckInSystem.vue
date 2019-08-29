<template>
    <div class="checkinsystem">
        <a-breadcrumb style="margin: 16px 0">
            <a-breadcrumb-item>选课系统</a-breadcrumb-item>
        </a-breadcrumb>
        <div :style="{ padding: '24px', background: '#fff', minHeight: '450px' }">
            <a-form class="ant-advanced-search-form" :form="form" @submit="handleSearch" :style="{padding: '24px'}">
                <div :style="{marginBottom:'30px'}">筛选课程</div>
                <a-row :gutter="24">
                    <a-col v-bind="formLayout">
                        <a-form-item label="课程名称">
                            <a-input placeholder="请输入课程名称" v-decorator="['name']"/>
                        </a-form-item>
                    </a-col>
                    <a-col v-bind="formLayout">
                        <a-form-item label="所属学校">
                            <a-input placeholder="请输入所属学校" v-decorator="['subordinateSchoolAndCollege']"/>
                        </a-form-item>
                    </a-col>
                    <a-col v-bind="formLayout">
                        <a-form-item label="模糊搜索">
                            <a-input placeholder="请输入要搜索的内容" v-decorator="['info']"/>
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
                <a-col v-bind="courseCardLayout" v-for="(item,index) in courseList" :key="index">
                    <a-card hoverable style="margin-top:10px ">
                        <template class="ant-card-actions" slot="actions">
                            <a-tooltip placement="top">
                                <template slot="title">
                                    <span>评论（暂未开放）</span>
                                </template>
                                <a-icon type="message" />
                            </a-tooltip>
                            <a-tooltip placement="top">
                                <template slot="title">
                                    <span>我要选课</span>
                                </template>
                                <a-icon type="link" @click="checkInClass(item)"/>
                            </a-tooltip>
                            <a-tooltip placement="top">
                                <template slot="title">
                                    <span>查看详情</span>
                                </template>
                                <a-icon type="ellipsis" @click="showDetail(item)"/>
                            </a-tooltip>
                        </template>

                        <div class="title"><img style="height: 25px; margin-right: 10px;"
                                                :src="imgpath.public.statistics"/>{{item.name}}
                        </div>
                        <div class="subtitle">{{item.subordinateSchoolAndCollege}}
                            <a-tag color="blue" style="margin-left: 10px">{{item.currentStatus}}</a-tag>
                        </div>
                        <div class="content">{{item.info}}</div>
                        <div class="footer">共{{item.checkInNum}}人选课</div>
                    </a-card>
                </a-col>
            </a-row>
            <a-row :gutter="24" type="flex" justify="end" style="margin-top: 12px">
                <a-pagination showSizeChanger showQuickJumper :pageSize.sync="pageSize"
                              @showSizeChange="onShowSizeChange" @change="onPageNumChange" :total="total"
                              v-model="current" :showTotal="total => `共 ${total} 条记录`"/>
            </a-row>
        </div>
        <a-modal v-if="visible" class="detail_modal" title="课程详情" v-model="visible">
            <template slot="footer">
                <a-button key="back" @click="visible = false">关闭</a-button>
                <a-button key="submit" type="primary" @click="checkInClass(courseInfo)">去选课</a-button>
            </template>

            <div class="title">{{courseInfo.name}}</div>
            <div class="subtitle">{{courseInfo.subordinateSchoolAndCollege}}
                <a-tag color="blue" style="margin-left: 10px">{{courseInfo.currentStatus}}</a-tag>
            </div>
            <div class="content">{{courseInfo.info}}</div>
            <div class="footer">共{{courseInfo.checkInNum}}人选课</div>
            <a-list
                    style="padding: 12px"
                    class="comment-list"
                    :header="`${data.length} 条评论`"
                    itemLayout="horizontal"
                    :dataSource="data"
            >
                <a-list-item slot="renderItem" slot-scope="item, index">
                    <a-comment
                            :author="item.author"
                            :avatar="item.avatar"
                    >
                        <template slot="actions">
                            <span v-for="action in item.actions">{{action}}</span>
                        </template>
                        <p slot="content">{{item.content}}</p>
                        <a-tooltip slot="datetime" :title="item.datetime.format('YYYY-MM-DD HH:mm:ss')">
                            <span>{{item.datetime.fromNow()}}</span>
                        </a-tooltip>
                    </a-comment>
                </a-list-item>
            </a-list>
        </a-modal>
    </div>
</template>

<script>
    import axios from 'axios'
    import moment from 'moment'
    import {Course, SelectionLog} from "../assets/js/url";

    export default {
        data() {
            return {
                data: [
                    {
                        actions: ['回复'],
                        author: '测试用户',
                        avatar: 'https://zos.alipayobjects.com/rmsportal/ODTLcjxAfvqbxHnVXCYX.png',
                        content: '这是一条评论',
                        datetime: moment().subtract(1, 'days'),
                    },
                ],
                moment,
                expand: false,
                form: this.$form.createForm(this),
                formLayout: {
                    lg: {span: 8},
                    md: {span: 24},
                },
                courseList: [],
                courseCardLayout: {
                    lg: {span: 12},
                    md: {span: 24}
                },
                pageSize: 10,
                current: 1,
                total: 0,
                visible: false,
                courseInfo: []
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
            showDetail(item) {
                this.courseInfo = item;
                this.visible = true;
            },
            checkInClass(item) {
                let formData = new FormData();
                formData.append('user', this.currentUserID);
                formData.append('selectedCourse', item.pk);
                formData.append('valid', '1');
                axios.post(SelectionLog, formData)
                    .then(
                        res => {
                            if (res.status === 201) {
                                this.$message.info("选课成功");
                                window.open(item.link, "_blank");
                            }
                        }
                    ).catch(
                    err => {
                        this.$message.error(err.response.data.detail);
                    }
                )
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
                        }
                    })
                    .catch(
                        err => {
                            that.$message.info(err.response.data.detail);
                        }
                    )
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
