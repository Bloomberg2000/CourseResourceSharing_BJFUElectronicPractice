<template>
    <div class="home">
        <a-breadcrumb style="margin: 16px 0">
            <a-breadcrumb-item>友情链接</a-breadcrumb-item>
        </a-breadcrumb>
        <div :style="{ padding: '24px', background: '#fff', minHeight: '450px' }">
            <a-row :gutter="24">
                <a-col v-bind="collegeCardLayout" v-for="(item,index) in collegeList" v-key="item">
                    <a-card hoverable style="margin-top:10px ">
                        <template class="ant-card-actions" slot="actions">
                            <a-tooltip placement="top">
                                <template slot="title">
                                    <span>前往</span>
                                </template>
                                <a-icon type="link"/>
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
        </div>

    </div>
</template>

<script>
    import axios from 'axios'
    import {College} from "../assets/js/url";

    export default {
        data() {
            return {
                collegeList: [],
                collegeCardLayout: {
                    lg: {span: 6},
                    md: {span: 8},
                    xs: {span: 24}
                },
            };
        },
        mounted() {
            this.getCollegeList();
        },
        methods: {
            getCollegeList() {
                let that = this;
                axios.get(College)
                    .then(
                        res => {
                            if (res.status === 200) {
                                that.collegeList = res.data;
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
