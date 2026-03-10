<template>
  <div style="padding: 24px;">
    <el-card>
      <template #header>
        <div style="display:flex;justify-content:space-between;align-items:center;">
          <span>项目列表</span>
          <el-button type="primary" @click="openCreate">新建项目</el-button>
        </div>
      </template>

      <el-table :data="projects" style="width: 100%;">
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="name" label="项目名" />
        <el-table-column prop="created_at" label="创建时间" />
        <el-table-column label="操作" width="180">
          <template #default="{ row }">
            <el-button size="small" @click="goProject(row.id)">打开</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <el-dialog v-model="visible" title="新建项目" width="420px">
      <el-form>
        <el-form-item label="项目名">
          <el-input v-model="name" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="visible = false">取消</el-button>
        <el-button type="primary" @click="createProject">创建</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { http } from '../api/http'

const router = useRouter()
const projects = ref<any[]>([])
const visible = ref(false)
const name = ref('')

const loadProjects = async () => {
  const res = await http.get('/projects')
  projects.value = res.data.data
}

const openCreate = () => {
  visible.value = true
}

const createProject = async () => {
  await http.post('/projects', { name: name.value })
  ElMessage.success('创建成功')
  visible.value = false
  name.value = ''
  await loadProjects()
}

const goProject = (id: number) => {
  router.push(`/projects/${id}`)
}

onMounted(loadProjects)
</script>