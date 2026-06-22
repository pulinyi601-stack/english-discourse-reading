import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { historyOperate } from '../api'

export const useHistoryStore = defineStore('history', () => {
  const list = ref([])
  const showPanel = ref(false)
  const isLoggedIn = computed(() => !!localStorage.getItem('token'))

  async function fetchList() {
    if (!isLoggedIn.value) return
    try {
      const res = await historyOperate('list')
      if (res.data.code === 200) list.value = res.data.data.history_list || []
    } catch { list.value = [] }
  }

  async function addRecord(taskId, textPreview, reportPreview) {
    if (!isLoggedIn.value) return
    try {
      await historyOperate('add', taskId)
      await fetchList()
    } catch { /* ignore */ }
  }

  async function deleteRecord(taskId) {
    try {
      await historyOperate('delete', taskId)
      await fetchList()
    } catch { /* ignore */ }
  }

  async function clearAll() {
    try {
      await historyOperate('clear')
      list.value = []
    } catch { /* ignore */ }
  }

  function togglePanel() { showPanel.value = !showPanel.value }

  return { list, showPanel, isLoggedIn, fetchList, addRecord, deleteRecord, clearAll, togglePanel }
})
