import axiosInstance from '@/axios'

export interface EbookRequest {
  id?: number
  user_id: number
  ebook_id: number
  request_date?: string
  return_date: string
  status?: string
}
export interface DBEbookRequest extends Omit<EbookRequest, 'id'> {
  id: number
}

// Create a new ebook request
export async function createEbookRequest(ebookRequest: EbookRequest) {
  const response = await axiosInstance.post('/ebook_requests', ebookRequest)
  return response.data
}

// Get all ebook requests
export async function getEbookRequests() {
  const response = await axiosInstance.get('/ebook_requests')
  return response.data as DBEbookRequest[]
}

// Get all ebook requests by user
export async function getEbookRequestsByUser() {
  const response = await axiosInstance.get(`/ebook_requests_user`)
  return response.data as DBEbookRequest[]
}

// Get an ebook request by ID
export async function getEbookRequestById(id: number) {
  const response = await axiosInstance.get(`/ebook_requests/${id}`)
  return response.data as DBEbookRequest
}

// Update an ebook request
export async function updateEbookRequest(ebookRequest: DBEbookRequest) {
  const response = await axiosInstance.put(`/ebook_requests/${ebookRequest.id}`, ebookRequest)
  return response.data
}

// Delete an ebook request
export async function deleteEbookRequest(id: number) {
  const response = await axiosInstance.delete(`/ebook_requests/${id}`)
  return response.data
}
