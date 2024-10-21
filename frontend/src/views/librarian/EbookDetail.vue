<template>
  <div class="container mt-3">
    <div class="row mb-3">
      <div class="col">
        <h1>Ebook Details: {{ ebook?.name }}</h1>
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
              {{ ebook?.name }}
            </div>
          </div>
          <div class="d-flex gap-3">
            <div class="w-25 text-end"><strong>Section Name:</strong></div>
            <div class="w-75">
              {{ section?.name }}
            </div>
          </div>
          <div class="d-flex gap-3">
            <div class="w-25 text-end"><strong>Author:</strong></div>
            <div class="w-75">
              {{ ebook?.author }}
            </div>
          </div>
          <div class="d-flex gap-3">
            <div class="w-25 text-end"><strong>Date Issued:</strong></div>
            <div class="w-75">
              {{ ebook?.date_issued }}
            </div>
          </div>
        </div>
        <h6 class="mt-4">Content:</h6>
        <p class="card-text">{{ ebook?.content }}</p>
        <div class="d-flex justify-content-end gap-2">
          <button class="btn btn-danger" @click="deleteEbookAPI(ebook?.id)">Delete</button>
          <button class="btn btn-warning" @click="goToUpdateEbook(ebook?.id)">Edit</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getEbookById, deleteEbook, type DBEbook } from '@/api/ebook'
import { push } from 'notivue'
import { getSectionById, type DBSection } from '@/api/section'

const route = useRoute()
const router = useRouter()

const ebook = ref<DBEbook | null>(null)
const section = ref<DBSection | null>(null)

const ebookId = computed(() => Number(route.params.ebookId))
const sectionId = computed(() => Number(route.params.sectionId))

const fetchEbookDetails = async () => {
  try {
    ebook.value = await getEbookById(ebookId.value)
  } catch (error) {
    console.error('Failed to fetch ebook details:', error)
  }
}

const fetchSectionDetails = async () => {
  try {
    section.value = await getSectionById(sectionId.value)
  } catch (error) {
    console.error('Failed to fetch section details:', error)
  }
}
const goBack = () => {
  router.go(-1)
}

const goToUpdateEbook = (id: number | undefined) => {
  if (id) {
    router.push({
      name: 'LibrarianEbookUpdate',
      params: { sectionId: sectionId.value, ebookId: ebookId.value }
    })
  }
}

const deleteEbookAPI = async (ebookId: number | undefined) => {
  if (ebookId) {
    try {
      await deleteEbook(ebookId)
      push.success('Ebook deleted successfully')
      router.push({
        name: 'LibrarianSectionDetail',
        params: { sectionId: ebook.value?.section_id }
      })
    } catch (error) {
      console.error('Failed to delete ebook:', error)
      push.error('Failed to delete ebook')
    }
  }
}

onMounted(() => {
  fetchEbookDetails()
  fetchSectionDetails()
})
</script>
