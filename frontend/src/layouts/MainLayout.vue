<template>
  <div class="app-container" :class="themeStore.currentTheme">
    <!-- Top Navigation -->
    <header class="top-nav">
      <div class="menu-toggle" @click="sidebarOpen = !sidebarOpen">
        <el-icon :size="22"><Fold v-if="sidebarOpen" /><Expand v-else /></el-icon>
      </div>
      <div class="logo-area">AI 英文语篇深度研读系统</div>
      <div class="spacer"></div>
      <div class="theme-switcher">
        <span style="font-size:13px;color:var(--text-secondary);margin-right:4px">主题</span>
        <div
          v-for="t in themeStore.themes"
          :key="t.key"
          class="theme-dot"
          :class="{ active: themeStore.currentTheme === t.key }"
          :style="{ backgroundColor: t.color }"
          :title="t.name"
          @click="themeStore.setTheme(t.key)"
        />
      </div>
    </header>

    <div class="body-wrapper">
      <!-- Sidebar -->
      <aside class="sidebar" :class="{ collapsed: !sidebarOpen }">
        <div class="menu-section">
          <div class="menu-section-title">辅助教学</div>
          <router-link
            v-for="item in teachingMenus"
            :key="item.path"
            :to="item.path"
            class="menu-item"
            :class="{ active: $route.path === item.path }"
          >
            <el-icon><component :is="item.icon" /></el-icon>
            <span>{{ item.label }}</span>
          </router-link>
        </div>
        <div class="menu-section">
          <div class="menu-section-title">辅助命题</div>
          <router-link
            v-for="item in examMenus"
            :key="item.path"
            :to="item.path"
            class="menu-item"
            :class="{ active: $route.path === item.path }"
          >
            <el-icon><component :is="item.icon" /></el-icon>
            <span>{{ item.label }}</span>
          </router-link>
        </div>
        <div class="menu-section">
          <div class="menu-section-title">其他</div>
          <router-link
            to="/free-chat"
            class="menu-item"
            :class="{ active: $route.path === '/free-chat' }"
          >
            <el-icon><ChatDotRound /></el-icon>
            <span>自由对话</span>
          </router-link>
        </div>
      </aside>

      <!-- Main Content -->
      <main class="main-content">
        <router-view />
      </main>
    </div>

    <!-- History Float Button -->
    <el-button
      class="history-float-btn"
      :icon="Clock"
      circle
      @click="historyStore.togglePanel()"
      title="历史记录"
    />
    <el-badge :value="historyStore.list.length" :hidden="historyStore.list.length === 0" class="history-badge">
    </el-badge>

    <!-- History Panel -->
    <div class="history-panel" :class="{ hidden: !historyStore.showPanel }">
      <div class="history-panel-header">
        <b>历史记录</b>
        <div>
          <el-button size="small" text @click="historyStore.clearAll()">清空</el-button>
          <el-button size="small" text @click="historyStore.togglePanel()">
            <el-icon><Close /></el-icon>
          </el-button>
        </div>
      </div>
      <div class="history-panel-body">
        <div v-if="historyStore.list.length === 0" style="text-align:center;color:var(--text-secondary);padding:40px 0;font-size:14px;">
          暂无历史记录
        </div>
        <div
          v-for="item in historyStore.list"
          :key="item.task_id"
          class="history-item"
          @click="restoreHistory(item)"
        >
          <div class="title">{{ item.text_preview || '未命名文本' }}</div>
          <div class="meta">{{ item.create_time }}</div>
          <div class="actions">
            <el-button size="small" text type="primary" @click.stop="restoreHistory(item)">查看</el-button>
            <el-button size="small" text type="danger" @click.stop="historyStore.deleteRecord(item.task_id)">删除</el-button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useThemeStore } from '../stores/theme'
import { useHistoryStore } from '../stores/history'
import { Clock, Fold, Expand, Close, ChatDotRound } from '@element-plus/icons-vue'

const themeStore = useThemeStore()
const historyStore = useHistoryStore()
const route = useRoute()
const router = useRouter()
const sidebarOpen = ref(true)

const teachingMenus = [
  { path: '/', label: '语篇深度研读报告', icon: 'Notebook' },
  { path: '/speech-analysis', label: '言说策略分析', icon: 'ChatLineSquare' },
  { path: '/language-points', label: '课文语言点讲解', icon: 'Reading' },
  { path: '/word-blocks', label: '词块教学', icon: 'Collection' },
  { path: '/essay-correction', label: '作文批改', icon: 'EditPen' },
  { path: '/exam-analysis', label: '试卷讲评', icon: 'DataAnalysis' },
  { path: '/teaching-design', label: '读写教学设计', icon: 'Document' },
  { path: '/image-gen', label: '图片生成', icon: 'Picture' },
]

const examMenus = [
  { path: '/reading-questions', label: '阅读设问', icon: 'QuestionFilled' },
  { path: '/text-adaptation', label: '文本改编', icon: 'CopyDocument' },
  { path: '/cloze-test', label: '完形命题', icon: 'List' },
  { path: '/bug-detection', label: '试题Bug检测', icon: 'WarningFilled' },
  { path: '/word-check', label: '超标词排查替换', icon: 'Search' },
]

function restoreHistory(item) {
  historyStore.togglePanel()
  router.push({ name: 'DeepReading', query: { task_id: item.task_id } })
}

onMounted(() => {
  document.documentElement.className = themeStore.currentTheme
  historyStore.fetchList()
})
</script>

<style scoped>
.history-float-btn {
  position: fixed;
  right: 20px;
  bottom: 30px;
  z-index: 80;
}
.sidebar a { text-decoration: none; }
</style>
