<template>
  <div class="container">
    <h1 class="my-4">Ebook Requests</h1>
    <b-table :items="ebookRequests" :fields="fields" responsive="sm">
      <template #cell(status)="{ item }">
        <b-badge :variant="getStatusVariant(item.status)">{{ item.status }}</b-badge>
      </template>
      <template #cell(actions)="{ item }">
        <b-button
          v-if="item.status === 'granted'"
          @click="returnEbook(item)"
          variant="primary"
          size="sm"
        >
          Return Ebook
        </b-button>
      </template>
    </b-table>

    <b-modal v-model="showFeedbackModal" title="Provide Feedback" @ok="submitFeedback">
      <b-form-textarea
        v-model="feedbackText"
        placeholder="Enter your feedback here..."
        rows="3"
        max-rows="6"
      ></b-form-textarea>
    </b-modal>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import {
  getEbookRequestsByUser,
  updateEbookRequest,
  type DBEbookRequest
} from '@/api/ebook_requests'
import { createFeedback } from '@/api/feedback'
import { push } from 'notivue'
import { getEbooks } from '@/api/ebook'

interface Ebook {
  id: number
  name: string
}

interface EbookRequest extends DBEbookRequest {
  ebook_name: string
}

const ebookRequests = ref<EbookRequest[]>([])
const showFeedbackModal = ref(false)
const feedbackText = ref('')
const currentEbookRequest = ref<EbookRequest | undefined>()

const fields = [
  { key: 'ebook_name', label: 'Ebook Name' },
  { key: 'request_date', label: 'Request Date' },
  { key: 'return_date', label: 'Return Date' },
  { key: 'status', label: 'Status' },
  { key: 'actions', label: 'Actions' }
]

const fetchEbookRequests = async () => {
  try {
    const [requestsData, ebooksData] = await Promise.all([getEbookRequestsByUser(), getEbooks()])

    const ebookMap: Record<number, string> = ebooksData.reduce(
      (acc: Record<number, string>, ebook: Ebook) => {
        acc[ebook.id] = ebook.name
        return acc
      },
      {}
    )

    ebookRequests.value = requestsData.map(
      (request: DBEbookRequest): EbookRequest => ({
        ...request,
        ebook_name: ebookMap[request.ebook_id] || 'Unknown Ebook'
      })
    )
  } catch (error) {
    console.error('Error fetching ebook requests:', error)
  }
}

const getStatusVariant = (status: EbookRequest['status']): string => {
  switch (status) {
    case 'requested':
      return 'warning'
    case 'granted':
      return 'success'
    case 'returned':
      return 'info'
    case 'expired':
    case 'revoked':
      return 'danger'
    case 'rejected':
      return 'secondary'
    default:
      return 'secondary'
  }
}

const returnEbook = async (item: EbookRequest) => {
  currentEbookRequest.value = item
  item.status = 'returned'
  item.return_date = new Date().toISOString()

  try {
    await updateEbookRequest(item)
    showFeedbackModal.value = true
  } catch (error) {
    console.error('Error returning ebook:', error)
  }
}

const submitFeedback = async () => {
  if (!feedbackText.value.trim()) {
    push.error('Please provide feedback before submitting.')
    return
  }

  if (!currentEbookRequest.value) {
    push.error('Please pick an ebook before submitting')
    return
  }

  try {
    await createFeedback({
      user_id: currentEbookRequest.value.user_id,
      ebook_id: currentEbookRequest.value.ebook_id,
      feedback: feedbackText.value,
      feedback_date: new Date().toISOString()
    })

    feedbackText.value = ''
    showFeedbackModal.value = false
    fetchEbookRequests()
  } catch (error) {
    console.error('Error submitting feedback:', error)
  }
}

onMounted(fetchEbookRequests)
</script>
