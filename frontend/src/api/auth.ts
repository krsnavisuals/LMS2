import axiosInstance from '@/axios'

export async function registerUser(username: string, password: string) {
  const response = await axiosInstance.post('/register-user', {
    username: username,
    password: password
  })
  return response.data
}

export async function loginUser(username: string, password: string) {
  const response = await axiosInstance.post('/login-user', {
    username: username,
    password: password
  })
  return response.data
}

export async function loginLibrarian(username: string, password: string) {
  const response = await axiosInstance.post('/login-librarian', {
    username: username,
    password: password
  })
  return response.data
}

export async function getUsers() {
  const response = await axiosInstance.get('/get-users')
  return response.data
}
