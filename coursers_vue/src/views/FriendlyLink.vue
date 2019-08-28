<template>
    <div class="home">
        <a-breadcrumb style="margin: 16px 0">
            <a-breadcrumb-item>友情链接</a-breadcrumb-item>
        </a-breadcrumb>
        <div :style="{ padding: '24px', background: '#fff', minHeight: '450px' }">
            <a-form layout="inline" :form="form" @submit="handleSearch"
                    :style="{padding: '24px'}">
                <a-form-item label="学校名称">
                    <a-input placeholder="请输入学校名称" v-decorator="['name']"/>
                </a-form-item>
                <a-form-item>
                    <a-button type="primary" html-type="submit">
                        搜索
                    </a-button>
                    <a-divider type="vertical"/>
                    <a-button  @click="handleReset">
                        清除
                    </a-button>
                </a-form-item>
            </a-form>
            <a-row :gutter="24" :style="{padding: '0 24px'}">
                <a-col v-bind="collegeCardLayout" v-for="(item,index) in collegeList" :key="index">
                    <a-card hoverable style="margin-top:10px ">
                        <img
                                alt="example"
                                :src="item.logoLink"
                                slot="cover"
                        />
                        <template class="ant-card-actions" slot="actions">
                            <a-tooltip placement="top">
                                <template slot="title">
                                    <span>前往</span>
                                </template>
                                <a-icon type="link" @click="goToLink(item.offcialLink)"/>
                            </a-tooltip>
                        </template>
                        <a-card-meta
                                :title="item.name"
                                :description="item.offcialLink">
                            <!--                    <a-avatar slot="avatar" src="https://zos.alipayobjects.com/rmsportal/ODTLcjxAfvqbxHnVXCYX.png"/>-->
                        </a-card-meta>
                    </a-card>
                </a-col>
            </a-row>
            <a-row :gutter="24" type="flex" justify="end" style="margin-top: 12px">
                <a-pagination showSizeChanger showQuickJumper :pageSize.sync="pageSize"
                              @showSizeChange="onShowSizeChange" @change="onPageNumChange" :total="total"
                              v-model="current" :showTotal="total => `共 ${total} 条记录`"/>
            </a-row>
        </div>

    </div>
</template>

<script>
    import axios from 'axios'
    import {College} from "../assets/js/url";

    export default {
        data() {
            return {
                form: this.$form.createForm(this),
                collegeList: [],
                collegeCardLayout: {
                    lg: {span: 6},
                    md: {span: 8},
                    xs: {span: 24}
                },
                pageSize: 10,
                current: 1,
                total: 0,
            };
        },
        mounted() {
            this.getCollegeList();
        },
        methods: {
            handleSearch(e) {
                this.current = 1;
                e.preventDefault();
                this.form.validateFields((error, values) => {
                    this.getCollegeList(values.name);
                });
            },
            handleReset() {
                this.current = 1;
                this.getCollegeList()
                this.form.resetFields();
            },
            onShowSizeChange(current, pageSize) {
                this.current = 1;
                this.getCollegeList()
            },
            onPageNumChange(pageNumber) {
                this.current = pageNumber;
                this.getCollegeList()
            },
            getCollegeList(name = "") {
                let that = this;
                axios.get(College, {
                    params: {
                        name: name,
                        size: this.pageSize,
                        page: this.current
                    }
                })
                    .then(
                        res => {
                            if (res.status === 200) {
                                that.total = res.data.count;
                                that.collegeList = res.data.results;
                            }
                        })
                    .catch(
                        err => {
                            that.$message.info(err.response.data.detail);
                        }
                    )
            },
            goToLink(link) {
                window.open(link, "_blank");
            }
        },
    };
</script>
