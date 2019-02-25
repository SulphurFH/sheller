<template>
  <el-container>
    <el-header class="header">
      <vheader/>
    </el-header>
    <el-container class="el-col-24 el-container-box">
      <el-aside width="200px" style="background-color:rgb(84, 92, 100);">
        <navmenu></navmenu>
      </el-aside>
      <el-main style="overflow-y:auto;">
        <router-view></router-view>
        <!-- <el-footer>Footer</el-footer> -->
      </el-main>
    </el-container>
  </el-container>
</template>

<script>
import Header from '@/components/Header'
import NavMenu from '@/components/NavMenu'

export default {
  name: 'Home',
  components: {
    'navmenu': NavMenu,
    'vheader': Header
  }
}

</script>

<style>
.header {
  background-color: #409EFF;
  color: #fff;
  line-height: 60px;
}
.el-container-box {
  position: absolute;
  top: 60px;
  bottom: 0;
}
</style>
