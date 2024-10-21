<template>
  <div class="container mt-4">
    <div class="d-flex justify-content-between">
      <h2>{{ isEditMode ? 'Update Section' : 'Add New Section' }}</h2>
      <button class="btn btn-secondary" @click="goBack()">Back</button>
    </div>
    <form @submit.prevent="handleSubmit">
      <div class="mb-3">
        <label for="sectionTitle" class="form-label">Title:</label>
        <input type="text" id="sectionTitle" v-model="section.name" class="form-control" required />
      </div>

      <div class="mb-3">
        <label for="sectionDescription" class="form-label">Description:</label>
        <textarea
          id="sectionDescription"
          v-model="section.description"
          class="form-control"
          rows="3"
          required
        ></textarea>
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
import { useRouter, useRoute } from 'vue-router'
import {
  createSection,
  getSectionById,
  updateSection,
  type DBSection,
  type Section
} from '@/api/section'
import { push } from 'notivue'

const router = useRouter()
const route = useRoute()

const isEditMode = ref(false)
const sectionId = parseInt(route.params.sectionId as string) || undefined

const goBack = () => {
  if (sectionId) router.push({ name: 'LibrarianSectionDetail', params: { sectionId: sectionId } })
  else router.push({ name: 'LibrarianDashboard' })
}

const section = ref<Section>({
  name: '',
  description: '',
  created_at: new Date()
})

const fetchSectionData = async (id: number) => {
  try {
    const data = await getSectionById(id)
    section.value = data
  } catch (error) {
    console.error('Failed to fetch section data:', error)
  }
}

onMounted(() => {
  if (sectionId) {
    isEditMode.value = true
    fetchSectionData(sectionId)
  }
})

const handleSubmit = async () => {
  try {
    if (isEditMode.value) {
      await updateSection(section.value as DBSection)
      push.success('Section updated successfully')
    } else {
      await createSection(section.value)
      push.success('Section created successfully')
    }
    goBack()
  } catch (error) {
    console.error(`Failed to ${isEditMode.value ? 'update' : 'add'} section:`, error)
  }
}
</script>
