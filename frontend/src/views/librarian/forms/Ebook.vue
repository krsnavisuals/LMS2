<template>
  <div class="container mt-4">
    <div class="d-flex justify-content-between">
      <h2>{{ isEditMode ? 'Update E-Book' : 'Add New E-Book' }}</h2>
      <button class="btn btn-secondary" @click="goBack()">Back</button>
    </div>
    <form @submit.prevent="handleSubmit">
      <div class="mb-3">
        <label for="ebookName" class="form-label">Ebook Name:</label>
        <input type="text" id="ebookName" v-model="ebook.name" class="form-control" required />
      </div>

      <div class="mb-3">
        <label for="ebookAuthor" class="form-label">Author:</label>
        <input type="text" id="ebookAuthor" v-model="ebook.author" class="form-control" required />
      </div>

      <div class="mb-3">
        <label for="ebookSection" class="form-label">Section:</label>
        <select id="ebookSection" v-model="ebook.section_id" class="form-select" required>
          <option v-for="section in sections" :key="section.id" :value="section.id">
            {{ section.name }}
          </option>
        </select>
      </div>

      <div class="mb-3">
        <label for="ebookContent" class="form-label">Content:</label>
        <textarea
          id="ebookContent"
          v-model="ebook.content"
          class="form-control"
          rows="5"
          required
        ></textarea>
      </div>

      <div class="mb-3">
        <label for="dateIssued" class="form-label">Date Issued:</label>
        <input
          type="date"
          id="dateIssued"
          v-model="ebook.date_issued"
          class="form-control"
          required
        />
      </div>

      <div class="d-flex justify-content-end mb-3">
        <button type="button" @click="goBack" class="btn btn-danger me-2">Cancel</button>
        <button type="submit" class="btn btn-success">{{ isEditMode ? 'Update' : 'Add' }}</button>
      </div>
    </form>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { createEbook, getEbookById, updateEbook, type DBEbook, type Ebook } from '@/api/ebook'
import { push } from 'notivue'
import { getSections, type DBSection } from '@/api/section'

const router = useRouter()
const route = useRoute()

const isEditMode = ref(false)
const ebookId = parseInt(route.params.ebookId as string) || undefined
const sectionId = parseInt(route.params.sectionId as string) || undefined

const goBack = () => {
  router.push({ name: 'LibrarianSectionDetail', params: { sectionId: sectionId } })
}

const formatDateTimeForInput = (date: Date): string => {
  return date.toISOString().slice(0, 10) // Format: YYYY-MM-DD
}
const ebook = ref<Ebook>({
  name: '',
  author: '',
  section_id: sectionId as number,
  content: '',
  date_issued: formatDateTimeForInput(new Date())
})

const sections = ref<DBSection[]>([])

const fetchSectionData = async () => {
  try {
    const data = await getSections()
    sections.value = data
  } catch (error) {
    console.error('failed to fetch section data:', error)
  }
}

const formatDateTimeForSubmission = (dateString: string): string => {
  const date = new Date(dateString)
  return date.toISOString().slice(0, 19).replace('T', ' ') // Format: YYYY-MM-DD HH:mm:ss
}

const fetchEbookData = async (id: number) => {
  try {
    const data = await getEbookById(id)
    ebook.value = {
      ...data,
      date_issued: formatDateTimeForInput(new Date(data.date_issued))
    }
  } catch (error) {
    console.error('Failed to fetch ebook data:', error)
  }
}

onMounted(async () => {
  fetchSectionData()
  if (ebookId) {
    isEditMode.value = true
    fetchEbookData(ebookId)
  }
})
const handleSubmit = async () => {
  try {
    const submissionData = {
      ...ebook.value,
      date_issued: formatDateTimeForSubmission(ebook.value.date_issued)
    }

    if (isEditMode.value) {
      await updateEbook(submissionData as DBEbook)
      push.success('Ebook updated successfully')
    } else {
      await createEbook(submissionData)
      push.success('Ebook created successfully')
    }
    goBack()
  } catch (error) {
    console.error(`Failed to ${isEditMode.value ? 'update' : 'add'} ebook:`, error)
  }
}
</script>
