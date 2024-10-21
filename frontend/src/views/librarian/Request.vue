<template>
  <div class="container">
    <h1 class="my-4">Librarian Ebook Request Management</h1>
    <b-table :items="ebookRequests" :fields="fields" responsive="sm">
      <template #cell(status)="{ item }">
        <b-badge :variant="getStatusVariant(item.status)">{{ item.status }}</b-badge>
      </template>
      <template #cell(actions)="{ item }">
        <div class="d-flex gap-2">
          <template v-if="item.status === 'requested'">
            <b-button @click="grantRequest(item)" variant="success" size="sm" class="mr-2">
              Grant
            </b-button>
            <b-button @click="rejectRequest(item)" variant="danger" size="sm"> Reject </b-button>
          </template>
          <b-button
            v-if="item.status === 'granted'"
            @click="revokeAccess(item)"
            variant="warning"
            size="sm"
          >
            Revoke
          </b-button>
          <b-button
            v-if="item.status === 'expired'"
            @click="revokeAccess(item)"
            variant="danger"
            size="sm"
          >
            Revoke Access
          </b-button>
        </div>
      </template>
    </b-table>

    <b-modal v-model="showConfirmModal" :title="confirmModalTitle" @ok="confirmAction">
      <p>{{ confirmModalMessage }}</p>
    </b-modal>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { getEbookRequests, updateEbookRequest } from '@/api/ebook_requests'
import { getUsers } from '@/api/auth'
import { getEbooks } from '@/api/ebook'

interface User {
  id: number
  username: string
}

interface Ebook {
  id: number
  name: string
}

// This interface represents the raw data returned from the API
interface DBEbookRequest {
  id: number
  user_id: number
  ebook_id: number
  request_date?: string
  return_date?: string
  status: 'requested' | 'granted' | 'returned' | 'expired' | 'rejected' | 'revoked'
}

// This interface represents the ebook request with additional fields we add
interface EbookRequest extends DBEbookRequest {
  username: string
  ebook_name: string
  request_date: string
  return_date: string
}

interface TableField {
  key: string
  label: string
}

const ebookRequests = ref<EbookRequest[]>([])
const showConfirmModal = ref(false)
const confirmModalTitle = ref('')
const confirmModalMessage = ref('')
const currentAction = ref<'grant' | 'reject' | 'revoke' | null>(null)
const currentItem = ref<EbookRequest | null>(null)

const fields: TableField[] = [
  { key: 'id', label: 'Request ID' },
  { key: 'username', label: 'User' },
  { key: 'ebook_name', label: 'Ebook' },
  { key: 'request_date', label: 'Request Date' },
  { key: 'return_date', label: 'Return Date' },
  { key: 'status', label: 'Status' },
  { key: 'actions', label: 'Actions' }
]

const fetchData = async (): Promise<void> => {
  try {
    const [requestsData, usersData, ebooksData] = await Promise.all([
      getEbookRequests(),
      getUsers(),
      getEbooks()
    ])

    const userMap: Record<number, string> = usersData.reduce(
      (acc: Record<number, string>, user: User) => {
        acc[user.id] = user.username
        return acc
      },
      {}
    )

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
        username: userMap[request.user_id] || 'Unknown User',
        ebook_name: ebookMap[request.ebook_id] || 'Unknown Ebook',
        request_date: request.request_date || 'N/A',
        return_date: request.return_date || 'N/A'
      })
    )

    console.log('Mapped ebook requests:', ebookRequests.value)
  } catch (error) {
    console.error('Error fetching data:', error)
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

const grantRequest = (item: EbookRequest): void => {
  currentAction.value = 'grant'
  currentItem.value = item
  confirmModalTitle.value = 'Confirm Grant Request'
  confirmModalMessage.value = `Are you sure you want to grant the ebook request for ${item.username}, Ebook: ${item.ebook_name}?`
  showConfirmModal.value = true
}

const rejectRequest = (item: EbookRequest): void => {
  currentAction.value = 'reject'
  currentItem.value = item
  confirmModalTitle.value = 'Confirm Reject Request'
  confirmModalMessage.value = `Are you sure you want to reject the ebook request for ${item.username}, Ebook: ${item.ebook_name}?`
  showConfirmModal.value = true
}

const revokeAccess = (item: EbookRequest): void => {
  currentAction.value = 'revoke'
  currentItem.value = item
  confirmModalTitle.value = 'Confirm Revoke Access'
  confirmModalMessage.value = `Are you sure you want to revoke access for ${item.username}, Ebook: ${item.ebook_name}?`
  showConfirmModal.value = true
}

const confirmAction = async (): Promise<void> => {
  if (!currentItem.value || !currentAction.value) return

  try {
    switch (currentAction.value) {
      case 'grant':
        currentItem.value.status = 'granted'
        break
      case 'reject':
        currentItem.value.status = 'rejected'
        break
      case 'revoke':
        currentItem.value.status = 'revoked'
        break
    }

    await updateEbookRequest(currentItem.value)
    await fetchData()
  } catch (error) {
    console.error(`Error ${currentAction.value}ing request:`, error)
  }

  showConfirmModal.value = false
}

onMounted(fetchData)
</script>
