<template>
  <div style="padding: 24px;">
    <el-card>
      <template #header>
        <div style="display:flex;justify-content:space-between;align-items:center;">
          <span>项目详情（占位）</span>
        </div>
      </template>

      <p>当前项目 ID：{{ projectId }}</p>
      <p style="color: #909399;">后续将在此处展示项目详情、文件列表与质检结果概览。</p>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const projectId = computed(() => route.params.id)

const loadProjectDetail = async () => {
  // TODO: 预留项目详情接口调用位置，例如：GET /projects/:id
  // await http.get(`/projects/${projectId.value}`)
}

onMounted(loadProjectDetail)
</script>
