<template>
  <el-row class="tac" height="100%">
    <el-col :span="24">
      <el-menu
        class="el-menu-vertical"
        style="border-right: 0;"
        @open="handleOpen"
        @close="handleClose"
        unique-opened
        router
        background-color="#545c64"
        text-color="#fff"
        active-text-color="#ffd04b">

        <el-submenu index="1">
          <template slot="title">
            <i class="el-icon-tickets"></i>
            <span>Task</span>
          </template>
          <el-menu-item-group class="over-hide">
            <el-menu-item index="/task/new_task">New Task</el-menu-item>
            <el-menu-item index="/task/task_lists">Task List</el-menu-item>
          </el-menu-item-group>
        </el-submenu>

        <el-submenu index="2">
          <template slot="title">
            <i class="el-icon-menu"></i>
            <span>Monitor</span>
          </template>
          <el-menu-item-group class="over-hide">
            <el-menu-item index="1-1">Celery</el-menu-item>
            <el-menu-item index="1-3">DB</el-menu-item>
            <el-menu-item index="1-4">Event Log</el-menu-item>
          </el-menu-item-group>
        </el-submenu>

      </el-menu>
    </el-col>
  </el-row>
</template>

<style scoped>
  .over-hide{
    overflow: hidden;
  }
</style>

<script>

export default {
  methods: {
    handleOpen (key, keyPath) {},
    handleClose (key, keyPath) {}
  }
}
</script>
