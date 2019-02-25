<template>
  <el-form :model="createTaskForm" :rules="rules" ref="createTaskForm" label-width="100px" class="demo-ruleForm">
    <el-form-item label="图片描述" prop="desc">
      <el-input type="textarea" v-model="createTaskForm.desc" style="max-width: 400px"></el-input>
    </el-form-item>
    <el-form-item label="上传图片" prop="image_path">
      <el-upload
        class="image-uploader"
        action="http://127.0.0.1:5000/api/upload"
        :show-file-list="false"
        :on-success="handleFileSuccess"
        :on-error="handleFileError"
        :before-upload="beforeAvatarUpload">
        <img v-if="imageUrl" :src="imageUrl" class="image">
        <i v-else class="el-icon-plus image-uploader-icon"></i>
      </el-upload>
    </el-form-item>
    <el-form-item>
      <el-button type="primary" @click="submitForm('createTaskForm')">立即创建</el-button>
      <el-button @click="resetForm('createTaskForm')">重置</el-button>
    </el-form-item>
  </el-form>
</template>

<style>
  .image-uploader .el-upload {
    border: 1px dashed #d9d9d9;
    border-radius: 6px;
    cursor: pointer;
    position: relative;
    overflow: hidden;
  }
  .image-uploader .el-upload:hover {
    border-color: #409EFF;
  }
  .image-uploader-icon {
    font-size: 28px;
    color: #8c939d;
    width: 178px;
    height: 178px;
    line-height: 178px;
    text-align: center;
  }
  .image {
    width: 178px;
    height: 178px;
    display: block;
  }
</style>

<script>
export default {
  data () {
    return {
      imageUrl: '',
      createTaskForm: {
        image_path: '',
        desc: ''
      },
      rules: {
        desc: [
          { required: true, max: 32, message: '请填写图片描述 ', trigger: 'blur' }
        ],
        image_path: [
          { required: true, max: 100, message: '请上传图片', trigger: 'change' }
        ]
      }
    }
  },
  methods: {
    submitForm (formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          this.createTask()
        } else {
          this.$message.error('参数错误，请检查参数')
          return false
        }
      })
    },
    resetForm (formName) {
      this.$refs[formName].resetFields()
      this.imageUrl = ''
    },
    handleFileSuccess (res, file) {
      this.imageUrl = URL.createObjectURL(file.raw)
      this.createTaskForm.image_path = res.file_name
    },
    // eslint-disable-next-line
    handleFileError (err, file) {
      this.$message.error('上传图片失败，请稍后重试！')
    },
    beforeAvatarUpload (file) {
      const isJPG = file.type === 'image/jpeg'
      const isPNG = file.type === 'image/png'
      const isLt2M = file.size / 1024 / 1024 < 2

      if (!isJPG && !isPNG) {
        this.$message.error('上传图片只能是 JPG/PNG 格式!')
      }
      if (!isLt2M) {
        this.$message.error('上传图片大小不能超过 2MB!')
      }
      return (isJPG || isPNG) && isLt2M
    },
    createTask () {
      let submitData = JSON.parse(JSON.stringify(this.createTaskForm))
      this.$axios.post(this.$httpConfig.SHELLER_HOST + '/api/tasks', submitData, {
        transformRequest: (data) => {
          return this.$qs.stringify(data)
        }
      }).then((res) => {
        if (res.status === 200) {
          this.$message.success('新建成功！')
          this.$router.push({path: '/task/task_lists'})
        } else {
          this.$message.error(res.data.message)
        }
        // eslint-disable-next-line
      }).catch((err) => {
        this.$message.error({
          type: 'info',
          message: '网络繁忙，请稍后再试...'
        })
      })
    }
  }
}
</script>
