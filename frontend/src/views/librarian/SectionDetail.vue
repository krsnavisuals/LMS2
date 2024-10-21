<template>
  <div class="container mt-3">
    <div class="row mb-3">
      <div class="col">
        <h1>Section Details: {{ section?.name }}</h1>
      </div>
      <div class="col-auto">
        <button class="btn btn-secondary" @click="goBack">Back</button>
      </div>
    </div>

    <div class="card mb-4">
      <div class="card-body">
        <div class="d-flex flex-column">
          <div class="d-flex gap-3">
            <div class="w-25 text-end"><strong>Title:</strong></div>
            <div class="w-75">
              {{ section?.name }}
            </div>
          </div>
          <div class="d-flex gap-3">
            <div class="w-25 text-end"><strong>Created At:</strong></div>
            <div class="w-75">
              {{ section?.created_at }}
            </div>
          </div>
          <div class="d-flex gap-3">
            <div class="w-25 text-end"><strong>Description:</strong></div>
            <div class="w-75">
              {{ section?.description }}
            </div>
          </div>
        </div>
        <div class="d-flex justify-content-end gap-2">
          <button class="btn btn-danger" @click="deleteSectionAPI(section?.id)">Delete</button>
          <button class="btn btn-warning" @click="goToUpdateSection(section?.id)">Edit</button>
        </div>
      </div>
    </div>

    <h2>Ebooks in this Section</h2>

    <div class="row mb-3 align-items-center">
      <div class="col">
        <input type="text" class="form-control" v-model="searchQuery" placeholder="Search ebooks" />
      </div>
    </div>

    <div class="row">
      <div class="col-md-4 mb-3" v-for="ebook in filteredEbooks" :key="ebook.id">
        <div class="card">
          <div class="card-body">
            <h5 class="card-title">{{ ebook.name }}</h5>
            <p class="card-text">Author: {{ ebook.author }}</p>
            <p class="card-text">Date Issued: {{ ebook.date_issued }}</p>
            <div class="d-flex justify-content-end gap-2">
              <button class="btn btn-danger" @click="deleteEbookAPI(ebook.id)">Delete</button>
              <button class="btn btn-warning" @click="goToUpdateEbook(ebook.id)">Edit</button>
              <button class="btn btn-primary" @click="viewEbookDetails(ebook.id)">Details</button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="row mt-3">
      <div class="col text-center">
        <button
          class="btn btn-lg btn-outline-primary rounded-circle p-2"
          @click="goToCreateEbook(section?.id)"
        >
          <v-icon name="hi-plus" scale="2.3"></v-icon>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { deleteSection, getSectionById, type DBSection } from '@/api/section'
import { getEbooksBySectionId, deleteEbook, type DBEbook } from '@/api/ebook'
import { push } from 'notivue'

const route = useRoute()
const router = useRouter()

const section = ref<DBSection | null>(null)
const ebooks = ref<DBEbook[]>([])
const searchQuery = ref('')

const sectionId = computed(() => Number(route.params.sectionId))

const fetchSectionDetails = async () => {
  try {
    section.value = await getSectionById(sectionId.value)
    ebooks.value = await getEbooksBySectionId(sectionId.value)
  } catch (error) {
    console.error('Failed to fetch section details:', error)
    push.error('Failed to load section details')
  }
}

const filteredEbooks = computed(() => {
  return ebooks.value.filter(
    (ebook) =>
      ebook.name.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
      ebook.author.toLowerCase().includes(searchQuery.value.toLowerCase())
  )
})

const goBack = () => {
  router.push({ name: 'LibrarianDashboard' })
}

const goToUpdateSection = (id: number | undefined) => {
  if (id) {
    router.push({ name: 'LibrarianSectionUpdate', params: { sectionId: id } })
  }
}

const goToCreateEbook = (sectionId: number | undefined) => {
  if (sectionId) {
    router.push({ name: 'LibrarianEbookCreate', params: { sectionId } })
  }
}

const goToUpdateEbook = (id: number | undefined) => {
  if (id) {
    router.push({
      name: 'LibrarianEbookUpdate',
      params: { sectionId: sectionId.value, ebookId: id }
    })
  }
}

const viewEbookDetails = (ebookId: number) => {
  router.push({ name: 'LibrarianEbookDetail', params: { ebookId } })
}

const deleteSectionAPI = async (sectionId: number | undefined) => {
  if (sectionId) {
    await deleteSection(sectionId)
    router.push({})
  }
}

const deleteEbookAPI = async (ebookId: number) => {
  await deleteEbook(ebookId)
  ebooks.value = await getEbooksBySectionId(sectionId.value)
  push.success('Ebook deleted successfully')
}

onMounted(() => {
  fetchSectionDetails()
})
</script>
