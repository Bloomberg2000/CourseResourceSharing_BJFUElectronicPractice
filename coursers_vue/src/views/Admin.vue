<template>
    <div class="home">
        <a-breadcrumb style="margin: 16px 0">
            <a-breadcrumb-item>后台管理</a-breadcrumb-item>
        </a-breadcrumb>
        <div :style="{ padding: '24px', background: '#fff', minHeight: '450px' }">
            <a-menu v-model="current" mode="horizontal">
                <a-menu-item key="course">
                    <a-icon type="file-search"/>
                    课程信息管理
                </a-menu-item>
                <a-menu-item key="college">
                    <a-icon type="appstore"/>
                    学校信息管理
                </a-menu-item>
            </a-menu>
            <CourseAdmin v-if="current[0] === 'course'"/>
            <CollegeAdmin v-else/>
        </div>
    </div>
</template>
<script>
    const CourseAdmin = () => import('../components/CourseAdmin');
    const CollegeAdmin = () => import('../components/CollegeAdmin');

    export default {
        components: {
            CourseAdmin, CollegeAdmin
        },
        data() {
            return {
                current: ['course'],
            }
        }
    }
</script>
