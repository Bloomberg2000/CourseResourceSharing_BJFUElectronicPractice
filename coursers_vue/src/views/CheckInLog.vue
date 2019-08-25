<template>
    <div class="home">
        <a-breadcrumb style="margin: 16px 0">
            <a-breadcrumb-item>选课记录</a-breadcrumb-item>
        </a-breadcrumb>
        <div :style="{ padding: '24px', background: '#fff', minHeight: '450px' }">
            <a-table bordered :dataSource="checkInLog" :columns="columns">
                <template slot="operation" slot-scope="text, record">
                    <a-popconfirm
                            v-if="checkInLog.length"
                            title="确定要删除这条记录吗？"
                            @confirm="() => onDelete(record.key)">
                        <a href="javascript:;">删除</a>
                    </a-popconfirm>
                </template>
            </a-table>
        </div>

    </div>
</template>

<script>
    import axios from 'axios'
    import {SelectionLog} from "../assets/js/url";

    export default {
        data() {
            return {
                checkInLog: [],
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
            };
        },
        mounted() {
            this.getSelectionLogList();
        },
        methods: {
            convertUTCDateToLocalDate(date) {
                let localTime = date;
                localTime = localTime.substr(0, date.lastIndexOf('.'));
                localTime = localTime.replace('T', ' ');
                return localTime;
            },
            getSelectionLogList() {
                let that = this;
                axios.get(SelectionLog)
                    .then(
                        res => {
                            if (res.status === 200) {
                                that.checkInLog = res.data;
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
                const checkInLog = [...this.checkInLog]
                this.checkInLog = checkInLog.filter(item => item.key !== key)
            },
        },
    };
</script>
