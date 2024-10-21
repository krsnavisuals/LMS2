import axiosInstance from '@/axios'

export interface Feedback {
  id?: number
  user_id: number
  ebook_id: number
  feedback: string
  feedback_date: string
}
export interface DBFeedback extends Omit<Feedback, 'id'> {
  id: number
}

// Create a new feedback entry
export async function createFeedback(feedback: Feedback) {
  const response = await axiosInstance.post('/feedback', feedback)
  return response.data
}

// Get all feedback entries
export async function getFeedback() {
  const response = await axiosInstance.get('/feedback')
  return response.data as DBFeedback[]
}

// Get a feedback entry by ID
export async function getFeedbackById(id: number) {
  const response = await axiosInstance.get(`/feedback/${id}`)
  return response.data as DBFeedback
}

// Update a feedback entry
export async function updateFeedback(feedback: DBFeedback) {
  const response = await axiosInstance.put(`/feedback/${feedback.id}`, feedback)
  return response.data
}

// Delete a feedback entry
export async function deleteFeedback(id: number) {
  const response = await axiosInstance.delete(`/feedback/${id}`)
  return response.data
}
