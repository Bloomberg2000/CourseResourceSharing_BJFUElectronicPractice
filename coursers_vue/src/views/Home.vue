<template>
    <div class="home">
        <a-breadcrumb style="margin: 16px 0">
            <a-breadcrumb-item>选课系统</a-breadcrumb-item>
        </a-breadcrumb>
        <div :style="{ padding: '24px', background: '#fff', minHeight: '450px' }">
            <a-table :columns="columns" :dataSource="data" :scroll="{ y: 400 }">
                <div slot="detail" slot-scope="text">
                    <a-button size="default">查看详情</a-button>
                    <a-divider type="vertical"></a-divider>
                    <a-button type="primary" size="default">我要选课</a-button>
                </div>
            </a-table>
        </div>
    </div>
</template>

<script>
    const columns = [{
        title: 'Name',
        dataIndex: 'name',
        width: 150,
    }, {
        title: 'Age',
        dataIndex: 'age',
        width: 150,
    }, {
        title: 'Address',
        dataIndex: 'address',
    }, {
        title: 'Action',
        key: 'operation',
        fixed: 'right',
        width: 300,
        scopedSlots: {customRender: 'detail'},
    },];

    const data = [];
    for (let i = 0; i < 100; i++) {
        data.push({
            key: i,
            name: `Edward King ${i}`,
            age: 32,
            address: `London, Park Lane no. ${i}`,
        });
    }

    export default {
        data() {
            return {
                data,
                columns,
            }
        }
    }
</script>
