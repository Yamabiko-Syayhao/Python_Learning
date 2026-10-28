export type Role = 1 | 2 | 3

export const ROLE_OPTIONS: { label: string; value: Role }[] = [
  { label: '超级管理员', value: 1 },
  { label: '管理员', value: 2 },
  { label: '普通用户', value: 3 },
]

export function roleLabel(role?: number): string {
  return ROLE_OPTIONS.find((item) => item.value === Number(role))?.label ?? '未知角色'
}

export interface AdminUser {
  id: number
  name: string
  userName: string
  role: Role
  lastLoginAt?: string | null
  createdAt?: string | null
  createAt?: string | null
}

export interface AuthUser extends AdminUser {
  token: string
}

export interface LoginPayload {
  userName: string
  passWord: string
}

export interface AdminFormData extends LoginPayload {
  name: string
  role: Role | undefined
}

export interface AdminPayload extends LoginPayload {
  name: string
  role: Role
}

export interface AdminPage {
  list: AdminUser[]
  count: number
}

export function emptyAdminForm(): AdminFormData {
  return { name: '', userName: '', passWord: '', role: undefined }
}
