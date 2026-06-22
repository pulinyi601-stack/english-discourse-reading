<template>
  <div class="file-uploader">
    <!-- Upload Area -->
    <div
      class="upload-zone"
      :class="{ 'dragover': isDragging, 'has-file': uploadedFile }"
      @dragenter.prevent="onDragEnter"
      @dragover.prevent="isDragging = true"
      @dragleave.prevent="onDragLeave"
      @drop.prevent="onDrop"
      @click="openFilePicker"
    >
      <input
        ref="fileInput"
        type="file"
        accept=".txt,.docx,.pdf"
        hidden
        @change="onFileSelected"
      />

      <div v-if="!uploading && !uploadedFile" class="upload-hint">
        <el-icon :size="40" style="color: var(--accent-color); margin-bottom: 8px;">
          <UploadFilled />
        </el-icon>
        <p style="font-weight: 600; color: var(--text-primary);">点击或拖拽文件到此处</p>
        <p style="font-size: 12px; color: var(--text-secondary); margin-top: 4px;">
          支持 TXT / DOCX / PDF，最大 10MB
        </p>
      </div>

      <div v-if="uploading" class="upload-progress">
        <el-progress type="circle" :percentage="uploadPercent" :width="60" :stroke-width="6" />
        <p style="margin-top: 8px; font-size: 13px; color: var(--text-secondary);">
          正在解析文件...
        </p>
      </div>

      <div v-if="!uploading && uploadedFile" class="uploaded-info">
        <div class="file-icon-box">
          <el-icon :size="28" :color="fileIconColor">
            <component :is="fileIcon" />
          </el-icon>
        </div>
        <div class="file-details">
          <p class="file-name">{{ uploadedFile.name }}</p>
          <p class="file-size">{{ uploadedFile.size }}</p>
        </div>
        <el-button size="small" text type="danger" @click.stop="removeFile">
          <el-icon><Delete /></el-icon>
        </el-button>
      </div>
    </div>

    <p v-if="errorMsg" class="error-msg">
      <el-icon><WarningFilled /></el-icon> {{ errorMsg }}
    </p>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { uploadFile } from '../api/upload'
import { ElMessage } from 'element-plus'
import {
  UploadFilled, Delete, WarningFilled,
  Document, FolderOpened, Tickets
} from '@element-plus/icons-vue'

const emit = defineEmits(['text-extracted'])

const fileInput = ref(null)
const isDragging = ref(false)
const uploading = ref(false)
const uploadPercent = ref(0)
const uploadedFile = ref(null)
const errorMsg = ref('')

const fileIcon = computed(() => {
  if (!uploadedFile.value) return Document
  const name = uploadedFile.value.name?.toLowerCase() || ''
  if (name.endsWith('.docx')) return FolderOpened
  if (name.endsWith('.pdf')) return Tickets
  return Document
})

const fileIconColor = computed(() => {
  const name = uploadedFile.value?.name?.toLowerCase() || ''
  if (name.endsWith('.docx')) return '#2b5797'
  if (name.endsWith('.pdf')) return '#d32f2f'
  return 'var(--accent-color)'
})

function openFilePicker() {
  if (!uploading.value) fileInput.value?.click()
}

function onDragEnter() { isDragging.value = true }
function onDragLeave() { isDragging.value = false }
function onDrop(e) {
  isDragging.value = false
  const files = e.dataTransfer.files
  if (files.length > 0) handleFile(files[0])
}

function onFileSelected(e) {
  if (e.target.files.length > 0) handleFile(e.target.files[0])
}

function handleFile(file) {
  errorMsg.value = ''
  const ext = '.' + file.name.split('.').pop().toLowerCase()
  const allowed = ['.txt', '.docx', '.pdf']
  if (!allowed.includes(ext)) {
    errorMsg.value = `不支持 ${ext} 格式`
    return
  }
  if (file.size > 10 * 1024 * 1024) {
    errorMsg.value = '文件超过 10MB 限制'
    return
  }

  uploadedFile.value = {
    name: file.name,
    size: formatSize(file.size),
    raw: file
  }

  uploadAndExtract(file)
}

async function uploadAndExtract(file) {
  uploading.value = true
  uploadPercent.value = 0

  try {
    const res = await uploadFile(file, (e) => {
      if (e.total) uploadPercent.value = Math.round((e.loaded / e.total) * 50)
    })

    uploadPercent.value = 80

    if (res.data.code === 200) {
      uploadPercent.value = 100
      const text = res.data.data.text_content
      emit('text-extracted', text)
      ElMessage.success(`已提取 ${res.data.data.word_count} 个词`)
    } else {
      errorMsg.value = res.data.msg
      uploadedFile.value = null
    }
  } catch {
    errorMsg.value = '文件上传失败，请稍后重试'
    uploadedFile.value = null
  } finally {
    uploading.value = false
  }
}

function removeFile() {
  uploadedFile.value = null
  errorMsg.value = ''
  uploadPercent.value = 0
  if (fileInput.value) fileInput.value.value = ''
  emit('text-extracted', '')
}

function formatSize(bytes) {
  if (bytes < 1024) return bytes + ' B'
  if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB'
  return (bytes / 1024 / 1024).toFixed(1) + ' MB'
}
</script>

<style scoped>
.file-uploader { margin-bottom: 12px; }

.upload-zone {
  border: 2px dashed var(--border-color);
  border-radius: 12px;
  padding: 24px;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s;
  background: var(--bg-secondary);
}
.upload-zone:hover { border-color: var(--accent-color); background: var(--hover-bg); }
.upload-zone.dragover {
  border-color: var(--accent-color);
  background: var(--hover-bg);
  transform: scale(1.01);
}
.upload-zone.has-file { border-style: solid; padding: 12px 20px; }

.upload-hint { display: flex; flex-direction: column; align-items: center; }

.uploaded-info {
  display: flex;
  align-items: center;
  gap: 12px;
  text-align: left;
}

.file-icon-box {
  width: 44px; height: 44px; border-radius: 8px;
  background: var(--hover-bg);
  display: flex; align-items: center; justify-content: center;
  flex-shrink: 0;
}

.file-details { flex: 1; min-width: 0; }
.file-name { font-weight: 600; font-size: 14px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.file-size { font-size: 12px; color: var(--text-secondary); margin-top: 2px; }

.error-msg {
  margin-top: 6px; font-size: 13px; color: #d32f2f;
  display: flex; align-items: center; gap: 4px;
}
</style>
