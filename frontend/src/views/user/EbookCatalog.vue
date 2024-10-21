<template>
  <div class="container mt-3">
    <div class="row mb-3">
      <div class="col">
        <h1>E-Book Catalog</h1>
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
            <button
              v-if="
                !(
                  ebook.status == 'requested' ||
                  ebook.status == 'expired' ||
                  ebook.status == 'granted'
                )
              "
              class="btn btn-success"
              @click="goToRequest(ebook.id)"
            >
              Request
            </button>
            <button
              v-else-if="ebook.status == 'requested' || ebook.status == 'expired'"
              class="btn btn-warning"
              disabled
              @click="goToRequest(ebook.id)"
            >
              Requested
            </button>
            <button
              v-else-if="ebook.status == 'granted'"
              class="btn btn-primary"
              @click="goToEbookDetail(ebook.id, ebook.section_id)"
            >
              View
            </button>
            <button
              v-if="ebook.status == 'granted'"
              class="btn btn-success"
              @click="returnEbook(ebook.id)"
            >
              Return
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
import { getEbooksRequestedByUser, type DBEbookWithStatus } from '@/api/ebook'
import { getSections, type DBSection } from '@/api/section'
import { useAuthStore } from '@/stores/auth'
import { push } from 'notivue'
import { updateEbookRequest, type DBEbookRequest } from '@/api/ebook_requests'

const router = useRouter()
const ebooks = ref<DBEbookWithStatus[]>([])
const sections = ref<DBSection[]>([])
const searchQuery = ref('')
const selectedSection = ref('')
const selectedSearchField = ref('all')
const authStore = useAuthStore()

const fetchEbooks = async () => {
  if (!authStore.user) {
    push.error('You are not logged in.')
    return
  }
  try {
    ebooks.value = await getEbooksRequestedByUser(authStore.user.id)
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

const goToRequest = (ebookId: number) => {
  router.push({ name: 'UserRequest', params: { ebookId } })
}

const goToEbookDetail = (ebookId: number, sectionId: number) => {
  router.push({ name: 'UserEbookDetail', params: { ebookId, sectionId } })
}

const returnEbook = async (ebookId: number) => {
  try {
    // Find the ebook request associated with this ebook
    const ebookRequest = ebooks.value.find((ebook) => ebook.id === ebookId)

    if (!ebookRequest) {
      push.error('E-book request not found.')
      return
    }

    // Update the ebook request with the return date and status
    const updatedEbookRequest: DBEbookRequest = {
      ...ebookRequest,
      return_date: new Date().toISOString(), // Set the return date to now
      status: 'returned' // Update the status to 'returned'
    }

    await updateEbookRequest(updatedEbookRequest)

    // Show a success notification
    push.success('E-book returned successfully.')

    // Refresh the ebook list to reflect the updated status
    fetchEbooks()
  } catch (error) {
    console.error('Failed to return e-book:', error)
    push.error('Failed to return the e-book. Please try again.')
  }
}

onMounted(() => {
  fetchEbooks()
  fetchSections()
})
</script>
