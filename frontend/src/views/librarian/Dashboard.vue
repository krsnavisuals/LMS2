<template>
  <div class="container mt-3">
    <div class="row mb-3">
      <div class="col">
        <h1>Librarian's Dashboard</h1>
      </div>
      <div class="col-auto"></div>
    </div>

    <div class="row mb-3 align-items-center">
      <div class="col">
        <input
          type="text"
          class="form-control"
          v-model="searchQuery"
          placeholder="Search sections"
        />
      </div>
    </div>

    <div class="row">
      <div
        role="button"
        class="col-md-4 mb-3"
        v-for="section in filteredSections"
        :key="section.id"
      >
        <div class="card">
          <div class="card-body">
            <h5 class="card-title">{{ section.name }}</h5>
            <p class="card-text">Created At: {{ section.created_at }}</p>
            <p class="card-text">{{ section.description }}</p>
            <div class="d-flex justify-content-end gap-2">
              <button class="btn btn-danger" @click="deleteSectionAPI(section.id)">Delete</button>
              <button class="btn btn-warning" @click="goToUpdateSection(section.id)">Edit</button>
              <button class="btn btn-primary" @click="goToSectionDetail(section.id)">View</button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="row mt-3">
      <div class="col text-center">
        <button
          class="btn btn-lg btn-outline-primary rounded-circle p-2"
          @click="goToCreateSection"
        >
          <v-icon name="hi-plus" scale="2.3"></v-icon>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { deleteSection, getSections, type DBSection, type Section } from '@/api/section'
import { push } from 'notivue'
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'

const sections = ref<DBSection[]>([])
const router = useRouter()
const searchQuery = ref('')

const filteredSections = computed(() => {
  return sections.value.filter(
    (section) =>
      section.name.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
      section.description.toLowerCase().includes(searchQuery.value.toLowerCase())
  )
})

const fetchSections = async () => {
  sections.value = await getSections()
  console.log('fetching')
}

const goToCreateSection = () => {
  router.push({ name: 'LibrarianSectionCreate' })
}

const goToUpdateSection = (sectionId: number) => {
  router.push({ name: 'LibrarianSectionUpdate', params: { sectionId } })
}

const goToSectionDetail = (sectionId: number) => {
  router.push({ name: 'LibrarianSectionDetail', params: { sectionId } })
}

const deleteSectionAPI = async (sectionId: number | undefined) => {
  if (sectionId) {
    await deleteSection(sectionId)
    push.success('Section deleted successfully')
    await fetchSections()
  }
}

onMounted(() => {
  fetchSections()
})
</script>
