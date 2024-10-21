<template>
  <div class="container mt-4">
    <h2>Request an E-Book</h2>
    <form @submit.prevent="handleSubmit">
      <div class="mb-3">
        <label for="ebookSelect" class="form-label">Select E-Book:</label>
        <select
          id="ebookSelect"
          v-model="ebookRequest.ebook_id"
          class="form-select"
          required
          :disabled="!!ebookId"
        >
          <option value="">Choose an e-book</option>
          <option v-for="ebook in ebooks" :key="ebook.id" :value="ebook.id">
            {{ ebook.name }} by {{ ebook.author }}
          </option>
        </select>
      </div>

      <div class="mb-3">
        <label for="requestDate" class="form-label">Request Date:</label>
        <input
          type="date"
          id="requestDate"
          v-model="ebookRequest.request_date"
          class="form-control"
          required
          disabled
        />
      </div>

      <div class="mb-3">
        <label for="returnDate" class="form-label">Return Date:</label>
        <input
          type="date"
          id="returnDate"
          v-model="ebookRequest.return_date"
          class="form-control"
          required
        />
      </div>

      <div class="d-flex justify-content-end">
        <button type="button" @click="goBack" class="btn btn-secondary me-2">Cancel</button>
        <button type="submit" class="btn btn-primary">Submit Request</button>
      </div>
    </form>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { createEbookRequest, type EbookRequest } from '@/api/ebook_requests'
import { getEbookById, getEbooks, type DBEbook } from '@/api/ebook'
import { useAuthStore } from '@/stores/auth'
import { push } from 'notivue'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()

const ebookId = parseInt(route.params.ebookId as string) || undefined
const ebooks = ref<DBEbook[]>([])
const ebook = ref<DBEbook>()

const today = new Date().toISOString().split('T')[0]

const ebookRequest = ref<EbookRequest>({
  user_id: authStore.user?.id || 0,
  ebook_id: ebookId || 0,
  request_date: today,
  return_date: ''
})

const fetchEbooks = async () => {
  try {
    ebooks.value = await getEbooks()
  } catch (error) {
    console.error('Failed to fetch ebooks:', error)
    push.error('Failed to load e-books. Please try again.')
  }
}

const fetchEbook = async () => {
  if (!ebookId) {
    return
  }
  try {
    ebook.value = await getEbookById(ebookId)
    ebookRequest.value.ebook_id = ebookId
  } catch (error) {
    console.error('Failed to fetch ebook:', error)
  }
}

const handleSubmit = async () => {
  try {
    await createEbookRequest(ebookRequest.value)
    push.success('E-book request submitted successfully')
    goBack()
  } catch (error) {
    console.error('Failed to submit e-book request:', error)
  }
}

const goBack = () => {
  router.push({ name: 'UserCatalog' })
}

onMounted(() => {
  fetchEbooks()
  fetchEbook()
})
</script>
