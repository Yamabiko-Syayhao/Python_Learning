import axios, { type AxiosRequestConfig } from 'axios'
import { expireSession, readSession } from '@/utils/authSession'

export interface ApiEnvelope<T> {
  code?: number
  msg?: string
  data?: T
  meta?: { status: number; msg?: string }
}

// In development /api is forwarded by Vite to the address in the supplied PDF.
// Deployments may set VITE_API_BASE_URL to their API gateway.
export const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '/api'

export const http = axios.create({
  baseURL: API_BASE_URL,
  timeout: 15000,
  headers: { 'Content-Type': 'application/json' },
})

http.interceptors.request.use((config) => {
  const token = readSession()?.token
  if (token && !['/login', '/register'].includes(config.url ?? '')) {
    config.headers.set('token', token)
  }
  return config
})

http.interceptors.response.use(
  (response) => {
    const body = response.data as ApiEnvelope<unknown>
    const status = Number(body?.code ?? body?.meta?.status)
    if (status === 401) expireSession()
    if (status !== 200) {
      throw new Error(body?.msg || body?.meta?.msg || '接口返回异常，请稍后重试')
    }
    return response
  },
  (error: unknown) => {
    if (axios.isCancel(error)) return Promise.reject(error)
    if (axios.isAxiosError<ApiEnvelope<unknown>>(error)) {
      const status = error.response?.status
      const body = error.response?.data
      if (status === 401 || Number(body?.code ?? body?.meta?.status) === 401) {
        expireSession()
        return Promise.reject(new Error('登录已失效，请重新登录'))
      }
      const message =
        body?.msg ||
        body?.meta?.msg ||
        (error.code === 'ECONNABORTED'
          ? '请求超时，请稍后重试'
          : error.response
            ? `请求失败（${status}）`
            : '无法连接接口，请检查网络和服务地址')
      return Promise.reject(new Error(message))
    }
    return Promise.reject(error)
  },
)

export async function request<T>(config: AxiosRequestConfig): Promise<T> {
  const response = await http.request<ApiEnvelope<T>>(config)
  return response.data.data as T
}

export function errorMessage(error: unknown): string {
  return error instanceof Error ? error.message : '操作失败，请稍后重试'
}
