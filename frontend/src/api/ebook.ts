import axiosInstance from '@/axios'

export interface Ebook {
  id?: number
  section_id: number
  name: string
  content: string
  author: string
  date_issued: string
}

export interface DBEbook extends Omit<Ebook, 'id'> {
  id: number
}

// Create a new eBook
export async function createEbook(ebook: Ebook) {
  const response = await axiosInstance.post('/ebooks', ebook)
  return response.data
}

// Get all eBooks
export async function getEbooks() {
  const response = await axiosInstance.get('/ebooks')
  return response.data as DBEbook[]
}

// Get ebook by section id
export async function getEbooksBySectionId(sectionId: number) {
  const response = await axiosInstance.get('/ebooks', {
    params: {
      section_id: sectionId
    }
  })
  return response.data as DBEbook[]
}

// Get an eBook by ID
export async function getEbookById(id: number) {
  const response = await axiosInstance.get(`/ebooks/${id}`)
  return response.data as DBEbook
}

// Update an eBook
export async function updateEbook(ebook: DBEbook) {
  const response = await axiosInstance.put(`/ebooks/${ebook.id}`, ebook)
  return response.data
}

// Delete an eBook
export async function deleteEbook(id: number) {
  const response = await axiosInstance.delete(`/ebooks/${id}`)
  return response.data
}

export interface DBEbookWithStatus extends DBEbook {
  status?: string
}
// Get all ebooks that have been requested by a specific user
export async function getEbooksRequestedByUser(userId: number) {
  const response = await axiosInstance.get(`/ebooks/requests`)
  return response.data as DBEbookWithStatus[]
}

// Get all ebooks that have been given feedback by a specific user
export async function getEbooksFeedbackByUser(userId: number) {
  const response = await axiosInstance.get(`/ebooks/feedback/${userId}`)
  return response.data as DBEbook[]
}
