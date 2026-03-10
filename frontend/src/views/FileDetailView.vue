<template>
  <div style="padding: 24px;">
    <el-card>
      <template #header>
        <div style="display:flex;justify-content:space-between;align-items:center;">
          <span>文件详情（占位）</span>
        </div>
      </template>

      <p>当前文件 ID：{{ fileId }}</p>
      <p style="color: #909399;">后续将在此处展示文件元信息、检测结果与修复建议。</p>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const fileId = computed(() => route.params.id)

const loadFileDetail = async () => {
  // TODO: 预留文件详情接口调用位置，例如：GET /files/:id
  // await http.get(`/files/${fileId.value}`)
}

onMounted(loadFileDetail)
</script>
