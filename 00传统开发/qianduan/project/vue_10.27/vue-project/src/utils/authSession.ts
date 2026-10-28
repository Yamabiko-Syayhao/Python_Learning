import type { AuthUser } from '@/types/admin'

const SESSION_KEY = 'hainan-admin-session'
export const AUTH_EXPIRED_EVENT = 'hainan:auth-expired'

export function readSession(): AuthUser | null {
  try {
    const value = sessionStorage.getItem(SESSION_KEY)
    if (!value) return null
    const session = JSON.parse(value) as Partial<AuthUser>
    if (
      typeof session.token !== 'string' ||
      !session.token ||
      typeof session.id !== 'number' ||
      typeof session.userName !== 'string' ||
      typeof session.name !== 'string' ||
      ![1, 2, 3].includes(Number(session.role))
    )
      return null
    return session as AuthUser
  } catch {
    return null
  }
}

export function writeSession(user: AuthUser): void {
  // Only the server's session is stored; passwords are never persisted.
  sessionStorage.setItem(SESSION_KEY, JSON.stringify(user))
}

export function clearSession(): void {
  sessionStorage.removeItem(SESSION_KEY)
}

export function expireSession(): void {
  clearSession()
  window.dispatchEvent(new Event(AUTH_EXPIRED_EVENT))
}
