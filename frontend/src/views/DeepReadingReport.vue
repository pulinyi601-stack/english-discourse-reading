<template>
  <div class="report-page">
    <div class="input-section" v-if="!generating && !reportContent">
      <h2 style="margin-bottom:16px;color:var(--accent-color);">语篇深度研读报告</h2>
      <p style="margin-bottom:12px;color:var(--text-secondary);font-size:14px;">
        输入英文语篇，AI 自动基于 What / Why / How 三层维度生成标准化研读报告
      </p>
      <!-- File Upload -->
      <FileUploader @text-extracted="onFileTextExtracted" />

      <!-- Divider -->
      <div style="display:flex;align-items:center;gap:12px;margin:8px 0 12px;">
        <span style="flex:1;height:1px;background:var(--border-color);"></span>
        <span style="font-size:13px;color:var(--text-secondary);">或直接输入文本</span>
        <span style="flex:1;height:1px;background:var(--border-color);"></span>
      </div>

      <el-input
        type="textarea"
        :rows="10"
        v-model="inputText"
        placeholder="请粘贴英文语篇文本..."
        @input="onInputChange"
        resize="vertical"
        class="report-textarea"
      />
      <div class="input-stats">
        <span>总词数：<b>{{ wordCount }}</b></span>
        <span style="margin-left:16px;">总句数：<b>{{ sentenceCount }}</b></span>
      </div>
      <div class="input-actions" style="margin-top:16px;display:flex;gap:12px;align-items:center;">
        <el-button type="primary" size="large" :loading="generating" :disabled="!isValidEnglish" @click="startGenerate">
          生成研读报告
        </el-button>
        <el-tag v-if="!isValidEnglish && inputText" type="danger">请输入标准英文语篇</el-tag>
        <el-tag v-if="remainingQuota !== null" type="info">今日剩余次数：{{ remainingQuota }}</el-tag>
      </div>
    </div>

    <!-- Loading Progress -->
    <div v-if="generating && !reportContent" class="loading-section">
      <el-progress type="circle" :percentage="progressPercent" :status="progressStatus" />
      <p style="margin-top:16px;color:var(--text-secondary);">正在生成研读报告，请稍候...</p>
    </div>

    <!-- Report Display -->
    <div v-if="reportContent" class="report-section">
      <div class="report-toolbar">
        <h3 style="color:var(--accent-color);">研读报告</h3>
        <div style="display:flex;gap:8px;flex-wrap:wrap;">
          <el-button size="small" @click="copyReport" :icon="CopyDocument">
            {{ copied ? '已复制' : '复制报告' }}
          </el-button>
          <el-button size="small" @click="exportFile('word')" :icon="Document">导出 Word</el-button>
          <el-button size="small" @click="exportFile('pdf')" :icon="Document">导出 PDF</el-button>
          <el-button size="small" @click="exportFile('markdown')" :icon="Document">导出 Markdown</el-button>
          <el-button size="small" @click="saveHistory" :icon="FolderAdd">保存记录</el-button>
          <el-button size="small" text @click="resetAll" :icon="RefreshRight">重新生成</el-button>
        </div>
      </div>
      <div class="report-body" v-html="renderedHTML"></div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { textCheck, generateReport, queryProgress, exportReport } from '../api'
import { useHistoryStore } from '../stores/history'
import MarkdownIt from 'markdown-it'
import { ElMessage } from 'element-plus'
import FileUploader from '../components/FileUploader.vue'
import { CopyDocument, Document, FolderAdd, RefreshRight } from '@element-plus/icons-vue'

const md = new MarkdownIt({ html: true, linkify: true })
const route = useRoute()
const historyStore = useHistoryStore()

const inputText = ref('')
const wordCount = ref(0)
const sentenceCount = ref(0)
const isValidEnglish = ref(true)
const generating = ref(false)
const reportContent = ref('')
const taskId = ref('')
const progressPercent = ref(0)
const progressStatus = ref('')
const remainingQuota = ref(null)
const copied = ref(false)

const renderedHTML = computed(() => {
  if (!reportContent.value) return ''
  return md.render(reportContent.value)
})

function onInputChange() {
  const text = inputText.value.trim()
  if (!text) { wordCount.value = 0; sentenceCount.value = 0; isValidEnglish.value = true; return }
  wordCount.value = text.split(/\s+/).filter(w => w.length > 0).length
  sentenceCount.value = text.split(/[.!?]+/).filter(s => s.trim().length > 0).length
  isValidEnglish.value = /^[\s\S]*[a-zA-Z]{2,}[\s\S]*$/.test(text)
}

function onFileTextExtracted(text) {
  if (text) {
    inputText.value = text
    onInputChange()
  }
}

async function startGenerate() {
  const text = inputText.value.trim()
  if (!text) { ElMessage.warning('请输入英文文本'); return }
  if (!isValidEnglish.value) { ElMessage.warning('请输入标准英文语篇'); return }

  generating.value = true
  progressPercent.value = 0
  progressStatus.value = ''

  try {
    const checkRes = await textCheck(text)
    if (checkRes.data.code !== 200) {
      ElMessage.error(checkRes.data.msg)
      generating.value = false
      return
    }
    const checkData = checkRes.data.data
    if (checkData.risk_status === 'reject') {
      ElMessage.warning(checkData.risk_msg || '文本包含违规内容')
      generating.value = false
      return
    }

    const genRes = await generateReport(checkData.clean_text, checkData.word_count)
    if (genRes.data.code !== 200) {
      ElMessage.error(genRes.data.msg)
      generating.value = false
      return
    }
    const genData = genRes.data.data
    taskId.value = genData.task_id
    remainingQuota.value = genData.remain_quota

    // Poll for progress
    await pollProgress(taskId.value)
  } catch (e) {
    ElMessage.error('请求失败，请稍后重试')
    generating.value = false
  }
}

async function pollProgress(id) {
  return new Promise((resolve) => {
    const timer = setInterval(async () => {
      try {
        const res = await queryProgress(id)
        if (res.data.code !== 200) {
          clearInterval(timer)
          generating.value = false
          ElMessage.error(res.data.msg || '查询进度失败')
          resolve()
          return
        }
        const data = res.data.data
        progressPercent.value = data.progress_percent || 0

        if (data.task_status === 'success') {
          clearInterval(timer)
          reportContent.value = data.report_content || ''
          generating.value = false
          progressStatus.value = 'success'
          resolve()
        } else if (data.task_status === 'fail') {
          clearInterval(timer)
          generating.value = false
          progressStatus.value = 'exception'
          ElMessage.error(data.fail_reason || '生成失败，请稍后重试')
          resolve()
        }
      } catch {
        clearInterval(timer)
        generating.value = false
        ElMessage.error('网络异常，请稍后重试')
        resolve()
      }
    }, 2000)
  })
}

async function copyReport() {
  await navigator.clipboard.writeText(reportContent.value)
  copied.value = true
  ElMessage.success('已复制到剪贴板')
  setTimeout(() => copied.value = false, 2000)
}

async function exportFile(type) {
  try {
    const res = await exportReport(taskId.value, type, reportContent.value)
    if (res.data.code === 200) {
      const url = res.data.data.file_download_url
      window.open(url, '_blank')
      ElMessage.success('文件生成中，正在下载...')
    } else {
      ElMessage.warning(res.data.msg || '导出失败')
    }
  } catch {
    ElMessage.error('导出失败，请稍后重试')
  }
}

function saveHistory() {
  const preview = inputText.value.trim().slice(0, 50)
  historyStore.addRecord(taskId.value, preview, reportContent.value.slice(0, 100))
  ElMessage.success('已保存至历史记录')
}

function resetAll() {
  reportContent.value = ''
  taskId.value = ''
  progressPercent.value = 0
  generating.value = false
  copied.value = false
}

onMounted(() => {
  if (route.query.task_id) {
    taskId.value = route.query.task_id
    pollProgress(route.query.task_id)
  }
})
</script>

<style scoped>
.report-page { max-width: 960px; margin: 0 auto; }
.report-textarea { font-size: 15px; line-height: 1.7; }
.input-stats { margin-top: 8px; font-size: 13px; color: var(--text-secondary); }
.loading-section { display: flex; flex-direction: column; align-items: center; padding: 80px 0; }
.report-toolbar {
  display: flex; justify-content: space-between; align-items: center;
  flex-wrap: wrap; gap: 12px; margin-bottom: 16px;
  padding-bottom: 12px; border-bottom: 1px solid var(--border-color);
}
.report-body {
  line-height: 1.8; font-size: 15px;
}
.report-body :deep(h2) { color: var(--accent-color); margin: 20px 0 12px; padding-bottom: 6px; border-bottom: 2px solid var(--accent-light); }
.report-body :deep(h3) { color: var(--accent-color); margin: 16px 0 8px; }
.report-body :deep(h4) { margin: 12px 0 6px; }
.report-body :deep(ul), .report-body :deep(ol) { padding-left: 24px; margin: 8px 0; }
.report-body :deep(li) { margin: 4px 0; }
.report-body :deep(p) { margin: 8px 0; }
.report-body :deep(strong) { color: var(--accent-color); }
.report-body :deep(blockquote) {
  border-left: 4px solid var(--accent-light);
  padding: 8px 16px; margin: 12px 0; background: var(--hover-bg); border-radius: 4px;
}
.report-body :deep(table) {
  width: 100%; border-collapse: collapse; margin: 12px 0;
}
.report-body :deep(th), .report-body :deep(td) {
  border: 1px solid var(--border-color); padding: 8px 12px; text-align: left;
}
.report-body :deep(th) { background: var(--hover-bg); font-weight: 600; }
</style>
