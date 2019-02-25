import Vue from 'vue'
import Router from 'vue-router'
import Home from '@/components/Home'
import NotFound from '@/components/NotFound'

// 懒加载方式，当路由被访问的时候才加载对应组件
const NewTask = resolve => require(['@/components/task/NewTask'], resolve)
const TaskList = resolve => require(['@/components/task/TaskList'], resolve)

Vue.use(Router)

const router = new Router({
  mode: 'history',
  routes: [
    {
      path: '/',
      component: Home
    },
    {
      path: '/task',
      name: 'task',
      component: Home,
      children: [
        { path: 'new_task', component: NewTask, name: 'new-task' },
        { path: 'task_lists', component: TaskList, name: 'task-lists' }
      ]
    },
    {
      path: '*',
      component: NotFound
    }
  ]
})

export default router
