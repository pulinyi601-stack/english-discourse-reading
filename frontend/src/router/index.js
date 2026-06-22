import { createRouter, createWebHistory } from 'vue-router'
import MainLayout from '../layouts/MainLayout.vue'

const childRoutes = [
  {
    path: '/',
    name: 'DeepReading',
    component: () => import('../views/DeepReadingReport.vue'),
    meta: { title: '语篇深度研读报告' }
  },
  {
    path: '/speech-analysis',
    name: 'SpeechAnalysis',
    component: () => import('../views/PlaceholderPage.vue'),
    meta: { title: '言说策略分析' }
  },
  {
    path: '/language-points',
    name: 'LanguagePoints',
    component: () => import('../views/PlaceholderPage.vue'),
    meta: { title: '课文语言点讲解' }
  },
  {
    path: '/word-blocks',
    name: 'WordBlocks',
    component: () => import('../views/PlaceholderPage.vue'),
    meta: { title: '词块教学' }
  },
  {
    path: '/essay-correction',
    name: 'EssayCorrection',
    component: () => import('../views/PlaceholderPage.vue'),
    meta: { title: '作文批改' }
  },
  {
    path: '/exam-analysis',
    name: 'ExamAnalysis',
    component: () => import('../views/PlaceholderPage.vue'),
    meta: { title: '试卷讲评' }
  },
  {
    path: '/teaching-design',
    name: 'TeachingDesign',
    component: () => import('../views/PlaceholderPage.vue'),
    meta: { title: '读写教学设计' }
  },
  {
    path: '/image-gen',
    name: 'ImageGen',
    component: () => import('../views/PlaceholderPage.vue'),
    meta: { title: '图片生成' }
  },
  {
    path: '/reading-questions',
    name: 'ReadingQuestions',
    component: () => import('../views/PlaceholderPage.vue'),
    meta: { title: '阅读设问' }
  },
  {
    path: '/text-adaptation',
    name: 'TextAdaptation',
    component: () => import('../views/PlaceholderPage.vue'),
    meta: { title: '文本改编' }
  },
  {
    path: '/cloze-test',
    name: 'ClozeTest',
    component: () => import('../views/PlaceholderPage.vue'),
    meta: { title: '完形命题' }
  },
  {
    path: '/bug-detection',
    name: 'BugDetection',
    component: () => import('../views/PlaceholderPage.vue'),
    meta: { title: '试题Bug检测' }
  },
  {
    path: '/word-check',
    name: 'WordCheck',
    component: () => import('../views/PlaceholderPage.vue'),
    meta: { title: '超标词排查替换' }
  },
  {
    path: '/free-chat',
    name: 'FreeChat',
    component: () => import('../views/PlaceholderPage.vue'),
    meta: { title: '自由对话' }
  }
]

const routes = [
  {
    path: '/',
    component: MainLayout,
    children: childRoutes
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
