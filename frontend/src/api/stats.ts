import axiosInstance from '@/axios'
import { useAuthStore } from '@/stores/auth'

// Interfaces for Librarian Stats
export interface EbookActivity {
  name: string
  request_count: number
}

export interface TopBorrowedEbook {
  name: string
  borrow_count: number
}

export interface ActiveRequest {
  id: number
  user_id: number
  ebook_id: number
  request_date: string
  return_date: string
  status: string
}

export interface OverdueRequest extends ActiveRequest {}

export interface UserActivity {
  username: string
  total_requests: number
  granted_requests: number
}

export interface FeedbackOverview {
  name: string
  feedback_count: number
  last_feedback_date: string
}

export interface EbooksBySection {
  section_name: string
  ebook_count: number
}

// Interface for Librarian Stats Response
export interface LibrarianStats {
  total_ebooks: number
  total_sections: number
  ebook_activity: EbookActivity[]
  top_borrowed_ebooks: TopBorrowedEbook[]
  active_requests: ActiveRequest[]
  overdue_requests: OverdueRequest[]
  user_activity: UserActivity[]
  feedback_overview: FeedbackOverview[]
  ebooks_by_section: EbooksBySection[]
}

// Interfaces for User Stats
export interface BorrowingHistory {
  name: string
  request_date: string
  return_date: string
}

export interface ActiveUserRequest {
  name: string
  request_date: string
  return_date: string
}

export interface OverdueBook {
  name: string
  return_date: string
}

export interface FeedbackGiven {
  name: string
  feedback: string
  feedback_date: string
}

export interface TopRequestedEbook {
  name: string
  request_count: number
}

export interface RecentlyAddedEbook {
  name: string
  author: string
  date_issued: string
}

// Interface for User Stats Response
export interface UserStats {
  borrowing_history: BorrowingHistory[]
  active_requests: ActiveUserRequest[]
  overdue_books: OverdueBook[]
  feedback_given: FeedbackGiven[]
  top_requested_ebooks: TopRequestedEbook[]
  recently_added_ebooks: RecentlyAddedEbook[]
}

// API call to get librarian statistics
export async function getLibrarianStats() {
  const response = await axiosInstance.get('/stats/librarian', {
    headers: { Authorization: `Bearer ${useAuthStore().token}` }
  })
  return response.data as LibrarianStats
}

// API call to get user statistics
export async function getUserStats() {
  const response = await axiosInstance.get(`/stats/user`, {
    headers: { Authorization: `Bearer ${useAuthStore().token}` }
  })
  return response.data as UserStats
}
