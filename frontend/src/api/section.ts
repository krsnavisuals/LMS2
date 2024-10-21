import axiosInstance from '@/axios'

export interface Section {
  id?: number
  name: string
  description: string
  created_at: Date
}

export interface DBSection extends Omit<Section, 'id'> {
  id: number
}

// Create a new section
export async function createSection(section: Section) {
  const response = await axiosInstance.post('/sections', section)
  return response.data
}

// Get all sections
export async function getSections() {
  const response = await axiosInstance.get('/sections')
  return response.data as DBSection[]
}

// Get a section by ID
export async function getSectionById(id: number) {
  const response = await axiosInstance.get(`/sections/${id}`)
  return response.data as DBSection
}

// Update a section
export async function updateSection(section: DBSection) {
  const response = await axiosInstance.put(`/sections/${section.id}`, section)
  return response.data
}

// Delete a section
export async function deleteSection(id: number) {
  const response = await axiosInstance.delete(`/sections/${id}`)
  return response.data
}
