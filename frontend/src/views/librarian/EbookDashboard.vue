<template>
  <div class="container mt-3">
    <div class="row mb-3">
      <div class="col">
        <h1>E-Book Dashboard</h1>
      </div>
    </div>

    <div class="row mb-3">
      <div class="col-md-4">
        <input
          type="text"
          class="form-control"
          v-model="searchQuery"
          placeholder="Search e-books"
          @input="searchEbooks"
        />
      </div>
      <div class="col-md-3">
        <select class="form-select" v-model="selectedSection" @change="searchEbooks">
          <option value="">All Sections</option>
          <option v-for="section in sections" :key="section.id" :value="section.id">
            {{ section.name }}
          </option>
        </select>
      </div>
      <div class="col-md-3">
        <select class="form-select" v-model="selectedSearchField" @change="searchEbooks">
          <option value="all">All Fields</option>
          <option value="title">Title</option>
          <option value="author">Author</option>
        </select>
      </div>
    </div>

    <div class="row">
      <div class="col-md-4 mb-3" v-for="ebook in filteredEbooks" :key="ebook.id">
        <div class="card h-100">
          <div class="card-body">
            <h5 class="card-title">{{ ebook.name }}</h5>
            <h6 class="card-subtitle mb-2 text-muted">{{ ebook.author }}</h6>
            <p class="card-text">
              <strong>Section:</strong> {{ getSectionName(ebook.section_id) }}
            </p>
            <p class="card-text">
              <strong>Date Issued:</strong> {{ formatDate(ebook.date_issued) }}
            </p>
          </div>
          <div class="d-flex justify-content-end card-footer gap-2">
            <button class="btn btn-danger" @click="deleteEbookAPI(ebook.id, ebook.section_id)">
              Delete
            </button>
            <button class="btn btn-warning" @click="goToUpdateEbook(ebook.id, ebook.section_id)">
              Edit
            </button>
            <button class="btn btn-primary" @click="viewEbookDetails(ebook.id, ebook.section_id)">
              Details
            </button>
          </div>
        </div>
      </div>
    </div>

    <div v-if="filteredEbooks.length === 0" class="text-center mt-4">
      <p>No e-books found matching your search criteria.</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { deleteEbook, getEbooks, getEbooksBySectionId, type DBEbook } from '@/api/ebook'
import { deleteSection, getSections, type DBSection } from '@/api/section'
import { push } from 'notivue'

const router = useRouter()
const ebooks = ref<DBEbook[]>([])
const sections = ref<DBSection[]>([])
const searchQuery = ref('')
const selectedSection = ref('')
const selectedSearchField = ref('all')

const fetchEbooks = async () => {
  try {
    ebooks.value = await getEbooks()
    console.log('ebooks:', ebooks.value)
  } catch (error) {
    console.error('Failed to fetch ebooks:', error)
  }
}

const fetchSections = async () => {
  try {
    sections.value = await getSections()
  } catch (error) {
    console.error('Failed to fetch sections:', error)
  }
}

const filteredEbooks = computed(() => {
  return ebooks.value.filter((ebook) => {
    const matchesQuery =
      selectedSearchField.value === 'all'
        ? ebook.name.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
          ebook.author.toLowerCase().includes(searchQuery.value.toLowerCase())
        : selectedSearchField.value === 'title'
          ? ebook.name.toLowerCase().includes(searchQuery.value.toLowerCase())
          : ebook.author.toLowerCase().includes(searchQuery.value.toLowerCase())

    const matchesSection =
      selectedSection.value === '' || ebook.section_id === parseInt(selectedSection.value)

    return matchesQuery && matchesSection
  })
})

const searchEbooks = () => {
  // The filtering is done reactively by the computed property
  console.log('Searching ebooks with query:', searchQuery.value)
}

const formatDate = (dateString: string): string => {
  return new Date(dateString).toLocaleString()
}

const getSectionName = (sectionId: number): string => {
  const section = sections.value.find((s) => s.id === sectionId)
  return section ? section.name : 'Unknown Section'
}

const goToCreateEbook = (sectionId: number | undefined) => {
  if (sectionId) {
    router.push({ name: 'LibrarianEbookCreate', params: { sectionId } })
  }
}

const goToUpdateEbook = (id: number | undefined, sectionId: number) => {
  if (id) {
    router.push({
      name: 'LibrarianEbookUpdate',
      params: { sectionId: sectionId, ebookId: id }
    })
  }
}

const viewEbookDetails = (ebookId: number, sectionId: number) => {
  router.push({ name: 'LibrarianEbookDetail', params: { ebookId, sectionId } })
}

const deleteEbookAPI = async (ebookId: number, sectionId: number) => {
  await deleteEbook(ebookId)
  ebooks.value = await getEbooksBySectionId(sectionId)
  push.success('Ebook deleted successfully')
}

onMounted(() => {
  fetchEbooks()
  fetchSections()
})
</script>
