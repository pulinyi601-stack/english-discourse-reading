import axios from 'axios'

const BASE_URL = import.meta.env.VITE_API_BASE || ''

const api = axios.create({
  baseURL: `${BASE_URL}/api/v1/english`,
  timeout: 30000,
  headers: { 'Content-Type': 'application/json' }
})

api.interceptors.request.use(config => {
  const token = localStorage.getItem('token')
  if (token) config.headers.Authorization = token
  return config
})

const buildToken = () => localStorage.getItem('token') || ''
const userType = () => (localStorage.getItem('token') ? 'login' : 'visitor')

export const textCheck = (rawText) =>
  api.post('/text/check', { raw_text: rawText, user_type: userType() })

export const generateReport = (cleanText, wordCount) =>
  api.post('/report/generate', {
    clean_text: cleanText,
    text_word_num: wordCount,
    user_token: buildToken(),
    user_type: userType()
  })

export const queryProgress = (taskId) =>
  api.get('/report/progress', { params: { task_id: taskId } })

export const exportReport = (taskId, exportType, reportContent) =>
  api.post('/report/export', {
    task_id: taskId,
    export_type: exportType,
    report_content: reportContent
  })

export const historyOperate = (operateType, taskId = '') =>
  api.post('/history/operate', {
    operate_type: operateType,
    task_id: taskId,
    user_token: buildToken()
  })

export default api
