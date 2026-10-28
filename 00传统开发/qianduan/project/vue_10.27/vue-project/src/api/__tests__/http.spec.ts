import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { AxiosError, type InternalAxiosRequestConfig } from 'axios'
import { http, request } from '@/api/http'
import { AUTH_EXPIRED_EVENT, readSession, writeSession } from '@/utils/authSession'

const originalAdapter = http.defaults.adapter
const session = {
  id: 1,
  name: '测试用户',
  userName: 'test',
  role: 2 as const,
  token: 'session-token',
}

function respond(config: InternalAxiosRequestConfig, data: unknown, status = 200) {
  return { config, data, status, statusText: String(status), headers: {} }
}

beforeEach(() => sessionStorage.clear())
afterEach(() => {
  http.defaults.adapter = originalAdapter
  vi.restoreAllMocks()
  sessionStorage.clear()
})

describe('接口状态和登录失效处理', () => {
  it.each([
    { code: 200, data: { value: 1 } },
    { meta: { status: 200, msg: '成功' }, data: { value: 1 } },
  ])('只在成功时提取data: %j', async (body) => {
    http.defaults.adapter = async (config) => respond(config, body)
    await expect(request({ method: 'GET', url: '/admin' })).resolves.toEqual({ value: 1 })
  })

  it('HTTP成功但业务失败时保留服务端提示', async () => {
    http.defaults.adapter = async (config) => respond(config, { code: 101, msg: '用户名密码错误' })
    await expect(request({ method: 'POST', url: '/login' })).rejects.toThrow('用户名密码错误')
  })

  it('格式错误的响应不能被当作成功', async () => {
    http.defaults.adapter = async (config) => respond(config, 'upstream unavailable')
    await expect(request({ method: 'GET', url: '/admin' })).rejects.toThrow('接口返回异常')
  })

  it('业务401清除会话并通知路由层', async () => {
    writeSession(session)
    const listener = vi.fn()
    window.addEventListener(AUTH_EXPIRED_EVENT, listener)
    try {
      http.defaults.adapter = async (config) => respond(config, { code: 401, msg: 'token验证失败' })
      await expect(request({ method: 'GET', url: '/admin' })).rejects.toThrow('token验证失败')
      expect(readSession()).toBeNull()
      expect(listener).toHaveBeenCalledTimes(1)
    } finally {
      window.removeEventListener(AUTH_EXPIRED_EVENT, listener)
    }
  })

  it('HTTP401也清除会话并返回可理解的错误', async () => {
    writeSession(session)
    http.defaults.adapter = async (config) => {
      throw new AxiosError(
        'Unauthorized',
        'ERR_BAD_REQUEST',
        config,
        undefined,
        respond(config, { msg: 'Unauthorized' }, 401),
      )
    }
    await expect(request({ method: 'GET', url: '/admin' })).rejects.toThrow('登录已失效')
    expect(readSession()).toBeNull()
  })

  it('网络超时给出明确提示，保留有效登录', async () => {
    writeSession(session)
    http.defaults.adapter = async (config) => {
      throw new AxiosError('timeout', 'ECONNABORTED', config)
    }
    await expect(request({ method: 'GET', url: '/admin' })).rejects.toThrow('请求超时')
    expect(readSession()?.token).toBe(session.token)
  })

  it('损坏的会话数据按未登录处理', () => {
    sessionStorage.setItem('hainan-admin-session', 'invalid json')
    expect(readSession()).toBeNull()
    sessionStorage.setItem('hainan-admin-session', JSON.stringify({ ...session, role: 9 }))
    expect(readSession()).toBeNull()
    sessionStorage.setItem('hainan-admin-session', JSON.stringify({ ...session, token: '' }))
    expect(readSession()).toBeNull()
  })
})
