import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import axios, { type InternalAxiosRequestConfig } from 'axios'
import {
  createAdmin,
  deleteAdmin,
  getAdmins,
  getAllAdmins,
  loginAccount,
  registerAccount,
  updateAdmin,
} from '@/api/admin'
import { http } from '@/api/http'
import { readSession, writeSession } from '@/utils/authSession'
import type { AdminPayload } from '@/types/admin'

const originalAdapter = http.defaults.adapter
const payload: AdminPayload = {
  name: '测试用户',
  userName: 'test-user',
  passWord: 'test-password',
  role: 2,
}
const user = (id: number) => ({ id, name: `用户${id}`, userName: `user${id}`, role: 3 })
const session = { ...user(1), role: 3 as const, token: 'session-token' }

function respond(config: InternalAxiosRequestConfig, data: unknown) {
  return { config, data, status: 200, statusText: 'OK', headers: {} }
}

beforeEach(() => sessionStorage.clear())
afterEach(() => {
  http.defaults.adapter = originalAdapter
  vi.restoreAllMocks()
  sessionStorage.clear()
})

describe('管理员接口请求契约', () => {
  it('登录使用文档大小写字段，不附带旧token，并清除响应中的密码字段', async () => {
    writeSession(session)
    const adapter = vi.fn(async (config: InternalAxiosRequestConfig) =>
      respond(config, {
        code: 200,
        data: {
          ...user(8),
          role: '2',
          token: 'new-token',
          passWord: 'server-should-not-return-this',
        },
      }),
    )
    http.defaults.adapter = adapter
    const result = await loginAccount({ userName: payload.userName, passWord: payload.passWord })
    const config = adapter.mock.calls[0]![0]
    expect(config.method).toBe('post')
    expect(config.url).toBe('/login')
    expect(JSON.parse(config.data)).toEqual({
      userName: payload.userName,
      passWord: payload.passWord,
    })
    expect(config.headers.get('token')).toBeUndefined()
    expect(result.role).toBe(2)
    expect(result).not.toHaveProperty('passWord')
    writeSession(result)
    expect(JSON.stringify(readSession())).not.toContain('server-should-not-return-this')
  })

  it('登录响应没有token时拒绝建立会话', async () => {
    http.defaults.adapter = async (config) => respond(config, { code: 200, data: user(1) })
    await expect(loginAccount({ userName: 'test', passWord: 'test' })).rejects.toThrow('token')
    expect(readSession()).toBeNull()
  })

  it('注册发送数值角色，允许仅有code/msg的成功响应', async () => {
    writeSession(session)
    const adapter = vi.fn(async (config: InternalAxiosRequestConfig) =>
      respond(config, { code: 200, msg: '成功' }),
    )
    http.defaults.adapter = adapter
    await registerAccount(payload)
    const config = adapter.mock.calls[0]![0]
    expect(config.method).toBe('post')
    expect(config.url).toBe('/register')
    expect(JSON.parse(config.data)).toEqual(payload)
    expect(config.headers.get('token')).toBeUndefined()
  })

  it('列表使用GET query分页与token头，兼容字符串数字字段', async () => {
    writeSession(session)
    const adapter = vi.fn(async (config: InternalAxiosRequestConfig) =>
      respond(config, {
        code: 200,
        data: { list: [{ ...user(4), role: '1' }], count: '21' },
      }),
    )
    http.defaults.adapter = adapter
    const result = await getAdmins(3, 10)
    const config = adapter.mock.calls[0]![0]
    expect(config.method).toBe('get')
    expect(config.url).toBe('/admin')
    expect(config.params).toEqual({ page: 3, rows: 10 })
    expect(config.headers.get('token')).toBe('session-token')
    expect(config.headers.get('Authorization')).toBeUndefined()
    expect(result).toEqual({ list: [{ ...user(4), role: 1 }], count: 21 })
  })

  it('拒绝缺失列表或总数的响应', async () => {
    http.defaults.adapter = async (config) => respond(config, { code: 200, data: { list: null } })
    await expect(getAdmins(1, 10)).rejects.toThrow('返回格式')
  })

  it('创建、编辑、删除使用对应方法与JSON body，不拼接错误详情路径', async () => {
    const adapter = vi.fn(async (config: InternalAxiosRequestConfig) =>
      respond(
        config,
        config.method === 'delete'
          ? { data: null, meta: { status: 200, msg: '删除成功' } }
          : { code: 200 },
      ),
    )
    http.defaults.adapter = adapter
    await createAdmin(payload)
    await updateAdmin(42, payload)
    await deleteAdmin(42)
    expect(
      adapter.mock.calls.map(([config]) => ({
        method: config.method,
        url: config.url,
        body: JSON.parse(config.data),
      })),
    ).toEqual([
      { method: 'post', url: '/admin', body: payload },
      { method: 'put', url: '/admin', body: { id: 42, ...payload } },
      { method: 'delete', url: '/admin', body: { id: 42 } },
    ])
  })
})

describe('搜索所需的全量分页读取', () => {
  it('尊重服务器页大小上限，取全页并按ID去重', async () => {
    const pages = [
      [user(1), user(2)],
      [user(2), user(3)],
      [user(4), user(5)],
    ]
    const adapter = vi.fn(async (config: InternalAxiosRequestConfig) =>
      respond(config, {
        code: 200,
        data: { list: pages[Number(config.params.page) - 1], count: 6 },
      }),
    )
    http.defaults.adapter = adapter
    const result = await getAllAdmins()
    expect(adapter.mock.calls.map(([config]) => config.params)).toEqual([
      { page: 1, rows: 100 },
      { page: 2, rows: 2 },
      { page: 3, rows: 2 },
    ])
    expect(result.map((item) => item.id)).toEqual([1, 2, 3, 4, 5])
  })

  it('空数据只请求第一页', async () => {
    const adapter = vi.fn(async (config: InternalAxiosRequestConfig) =>
      respond(config, {
        code: 200,
        data: { list: [], count: 0 },
      }),
    )
    http.defaults.adapter = adapter
    expect(await getAllAdmins()).toEqual([])
    expect(adapter).toHaveBeenCalledTimes(1)
  })

  it('总数非零但首批为空时明确报错，避免显示不完整搜索结果', async () => {
    http.defaults.adapter = async (config) =>
      respond(config, {
        code: 200,
        data: { list: [], count: 10 },
      })
    await expect(getAllAdmins()).rejects.toThrow('无法完成搜索')
  })

  it('取消搜索不继续获取后续页，并保留Axios取消语义', async () => {
    const controller = new AbortController()
    const adapter = vi.fn(async (config: InternalAxiosRequestConfig) => {
      controller.abort()
      return respond(config, { code: 200, data: { list: [user(1)], count: 3 } })
    })
    http.defaults.adapter = adapter
    const error = await getAllAdmins(controller.signal).catch((reason: unknown) => reason)
    expect(axios.isCancel(error)).toBe(true)
    expect(adapter).toHaveBeenCalledTimes(1)
  })
})
