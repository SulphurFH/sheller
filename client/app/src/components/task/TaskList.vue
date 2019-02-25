<template>
  <section>
    <el-table
      :data="tableData"
      stripe
      style="width: 100%">
      <el-table-column
        prop="desc"
        label="描述"
        width="180">
      </el-table-column>
      <el-table-column
        prop="created_at"
        label="创建日期"
        width="180">
      </el-table-column>
      <el-table-column
        prop="edit"
        label="操作">
        <template slot-scope="scope">
          <el-button @click="handleClick(scope.row)" type="primary" size="small">查看</el-button>
          <el-button @click="handleDelete(scope.row)" type="danger" size="small">删除</el-button>
        </template>
      </el-table-column>
    </el-table>
    <div style="text-align: center;margin-top: 30px;">
      <el-pagination
        background
        layout="prev, pager, next"
        :page-size="pageSize"
        :total="total"
        @current-change="currentChange">
      </el-pagination>
    </div>
  </section>
</template>

<script>
export default {
  name: 'taskList',
  data () {
    return {
      tableData: [],
      total: 0,
      pageSize: 10,
      currentPage: 1
    }
  },
  methods: {
    getTaskList () {
      this.$axios.get(this.$httpConfig.SHELLER_HOST + '/api/tasks', {
        params: {
          page: this.currentPage,
          page_size: this.pageSize
        }
      }).then((res) => {
        if (res.status === 200) {
          this.tableData = res.data.results
          this.total = res.data.count
        } else {
          this.$message.error(res.data.message)
        }
        // eslint-disable-next-line
      }).catch((err) => {
        console.log(err)
        this.$message.error({
          type: 'info',
          message: '网络繁忙，请稍后再试...'
        })
      })
    },
    handleClick (val) {
      console.log(val.id)
    },
    handleDelete (val) {
      console.log(val.id)
    },
    currentChange (currentPage) {
      this.currentPage = currentPage
      this.getTaskList()
    }
  },
  mounted: function () {
    this.getTaskList()
  }
}
</script>
