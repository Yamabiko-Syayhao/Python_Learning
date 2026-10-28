import axios from 'axios'
import { request } from './http'
import type { AdminPage, AdminPayload, AdminUser, AuthUser, LoginPayload } from '@/types/admin'

export async function loginAccount(data: LoginPayload): Promise<AuthUser> {
  const user = await request<AuthUser>({ method: 'POST', url: '/login', data })
  if (
    !user ||
    typeof user.token !== 'string' ||
    !user.token.trim() ||
    !Number.isFinite(Number(user.id)) ||
    Number(user.id) <= 0 ||
    typeof user.name !== 'string' ||
    typeof user.userName !== 'string' ||
    !user.userName.trim() ||
    ![1, 2, 3].includes(Number(user.role))
  ) {
    throw new Error('登录响应缺少有效的用户信息或 token')
  }
  // Explicit fields prevent any unexpected response password from entering storage.
  return {
    id: Number(user.id),
    name: user.name,
    userName: user.userName,
    role: Number(user.role) as AuthUser['role'],
    token: user.token,
    lastLoginAt: user.lastLoginAt,
    createAt: user.createAt,
    createdAt: user.createdAt,
  }
}

export async function registerAccount(data: AdminPayload): Promise<void> {
  await request<void>({ method: 'POST', url: '/register', data })
}

export async function getAdmins(
  page: number,
  rows: number,
  signal?: AbortSignal,
): Promise<AdminPage> {
  const result = await request<AdminPage>({
    method: 'GET',
    url: '/admin',
    params: { page, rows },
    signal,
  })
  if (!result || !Array.isArray(result.list) || !Number.isFinite(Number(result.count))) {
    throw new Error('角色列表返回格式不正确')
  }
  return {
    count: Number(result.count),
    list: result.list.map((user) => ({ ...user, role: Number(user.role) as AdminUser['role'] })),
  }
}

// The PDF defines no search endpoint. Fetch every real page, then filter locally.
export async function getAllAdmins(signal?: AbortSignal): Promise<AdminUser[]> {
  const first = await getAdmins(1, 100, signal)
  const result = [...first.list]
  if (first.count === 0) return result
  // Respect a possible server-side maximum page size.
  const size = first.list.length
  if (!size) throw new Error('接口返回了空列表，无法完成搜索')
  const pages = Math.ceil(first.count / size)
  for (let page = 2; page <= pages; page += 1) {
    if (signal?.aborted) throw new axios.CanceledError()
    const next = await getAdmins(page, size, signal)
    if (!next.list.length) throw new Error('接口分页数据不完整，请刷新后重新搜索')
    result.push(...next.list)
  }
  return Array.from(new Map(result.map((user) => [user.id, user])).values())
}

export async function createAdmin(data: AdminPayload): Promise<void> {
  await request<void>({ method: 'POST', url: '/admin', data })
}

export async function updateAdmin(id: number, data: AdminPayload): Promise<void> {
  await request<void>({ method: 'PUT', url: '/admin', data: { id, ...data } })
}

export async function deleteAdmin(id: number): Promise<void> {
  await request<void>({ method: 'DELETE', url: '/admin', data: { id } })
}
