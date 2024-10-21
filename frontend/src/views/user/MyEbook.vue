<template>
  <div class="container mt-3">
    <div class="row mb-3">
      <div class="col">
        <h1>My Ebook</h1>
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
            <p class="card-text">
              <strong>Return Date:</strong> {{ formatDate(ebook.return_date) }}
            </p>
          </div>
          <div class="card-footer">
            <button class="btn btn-primary" @click="viewEbookDetails(ebook.id)">
              View Details
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
import { getEbooks, type DBEbook } from '@/api/ebook'
import { getSections, type DBSection } from '@/api/section'

const router = useRouter()
const ebooks = ref<DBEbook[]>([])
const sections = ref<DBSection[]>([])
const searchQuery = ref('')
const selectedSection = ref('')
const selectedSearchField = ref('all')

const fetchEbooks = async () => {
  try {
    ebooks.value = await getEbooks()
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

const viewEbookDetails = (ebookId: number) => {
  router.push({ name: 'LibrarianEbookDetail', params: { ebookId } })
}

onMounted(() => {
  fetchEbooks()
  fetchSections()
})
</script>
