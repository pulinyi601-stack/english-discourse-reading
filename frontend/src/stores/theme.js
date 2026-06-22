import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useThemeStore = defineStore('theme', () => {
  const themes = [
    { key: 'theme-green', name: '唐柳绿', color: '#6b8c5e' },
    { key: 'theme-blue', name: '海雾蓝', color: '#5b8ca8' },
    { key: 'theme-brown', name: '暖纸棕', color: '#a0845c' },
    { key: 'theme-pink', name: '樱粉柔光', color: '#c97b84' },
    { key: 'theme-dark', name: '午夜黑', color: '#0f3460' }
  ]
  const currentTheme = ref(localStorage.getItem('theme') || 'theme-green')

  function setTheme(key) {
    currentTheme.value = key
    localStorage.setItem('theme', key)
    document.documentElement.className = key
  }

  return { themes, currentTheme, setTheme }
})
