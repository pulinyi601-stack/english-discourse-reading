import axios from 'axios'

const BASE_URL = import.meta.env.VITE_API_BASE || ''

const api = axios.create({
  baseURL: `${BASE_URL}/api/v1/english`,
  timeout: 60000,
  headers: { 'Content-Type': 'multipart/form-data' }
})

export function uploadFile(file, onProgress) {
  const form = new FormData()
  form.append('file', file)
  return api.post('/file/upload', form, {
    headers: { 'Content-Type': 'multipart/form-data' },
    onUploadProgress: onProgress
  })
}
