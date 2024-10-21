import { jwtDecode } from 'jwt-decode'
import type { User } from '@/stores/auth.ts'
import type { JwtPayload } from 'jwt-decode'

export function getIdentityFromToken(token: string | null) {
  if (!token) return null

  try {
    const decodedToken = jwtDecode<JwtPayload>(token)
    return decodedToken.sub as unknown as User
  } catch (error) {
    console.error('Invalid token:', error)
    return null
  }
}
