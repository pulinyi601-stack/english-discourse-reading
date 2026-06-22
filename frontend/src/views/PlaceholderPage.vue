<template>
  <div style="display:flex;flex-direction:column;align-items:center;justify-content:center;padding:100px 0;color:var(--text-secondary);">
    <el-icon :size="60" style="margin-bottom:16px;opacity:0.4;"><Tools /></el-icon>
    <h3 style="margin-bottom:8px;">{{ route.meta.title || '功能开发中' }}</h3>
    <p>该功能将在 V2.0 迭代中上线，敬请期待</p>
  </div>
</template>

<script setup>
import { useRoute } from 'vue-router'
import { Tools } from '@element-plus/icons-vue'
const route = useRoute()
</script>
