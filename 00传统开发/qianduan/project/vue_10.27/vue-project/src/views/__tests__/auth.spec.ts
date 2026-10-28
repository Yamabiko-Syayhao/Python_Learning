import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { flushPromises, mount, type VueWrapper } from '@vue/test-utils'
import { createPinia } from 'pinia'
import { createMemoryHistory, createRouter } from 'vue-router'
import ElementPlus, { ElMessage } from 'element-plus'
import LoginView from '@/views/LoginView.vue'
import RegisterView from '@/views/RegisterView.vue'
import { loginAccount, registerAccount } from '@/api/admin'

vi.mock('@/api/admin', () => ({
  loginAccount: vi.fn(),
  registerAccount: vi.fn(),
}))

const wrappers: VueWrapper[] = []
const loggedInUser = {
  id: 42,
  name: '测试姓名',
  userName: 'test-account',
  role: 2 as const,
  token: 'test-token',
}

beforeEach(() => {
  vi.resetAllMocks()
  sessionStorage.clear()
  vi.mocked(loginAccount).mockResolvedValue(loggedInUser)
  vi.mocked(registerAccount).mockResolvedValue(undefined)
})

afterEach(() => {
  wrappers.splice(0).forEach((wrapper) => wrapper.unmount())
  ElMessage.closeAll()
  document.body.innerHTML = ''
  sessionStorage.clear()
})

async function openPage(path: string) {
  const router = createRouter({
    history: createMemoryHistory(),
    routes: [
      { path: '/login', component: LoginView },
      { path: '/register', component: RegisterView },
      { path: '/admin/roles', component: { template: '<p>角色列表测试页</p>' } },
    ],
  })
  await router.push(path)
  await router.isReady()
  const wrapper = mount(
    { template: '<RouterView />' },
    { attachTo: document.body, global: { plugins: [createPinia(), router, ElementPlus] } },
  )
  wrappers.push(wrapper)
  await flushPromises()
  return { wrapper, router }
}

function findButton(wrapper: VueWrapper, text: string) {
  const button = wrapper.findAll('button').find((item) => item.text() === text)
  if (!button) throw new Error(`未找到按钮：${text}`)
  return button
}

async function fillRegistration(wrapper: VueWrapper) {
  await wrapper.get('input[autocomplete="name"]').setValue('  测试姓名  ')
  await wrapper.get('input[autocomplete="username"]').setValue('  test-account  ')
  await wrapper.get('input[autocomplete="new-password"]').setValue('test-password')
}

async function chooseRole(wrapper: VueWrapper, label: string) {
  await wrapper.get('.el-select__wrapper').trigger('click')
  await flushPromises()
  const option = Array.from(
    document.querySelectorAll<HTMLElement>('.el-select-dropdown__item'),
  ).find((item) => item.textContent?.trim() === label)
  if (!option) throw new Error(`未找到角色选项：${label}`)
  option.click()
  await flushPromises()
}

describe('注册表单交互', () => {
  it('空表单和缺少角色时显示必填提示，并阻止注册请求', async () => {
    const { wrapper, router } = await openPage('/register')
    const submitButton = findButton(wrapper, '立即注册').element as HTMLButtonElement
    expect(submitButton.form).toBe(wrapper.get('form').element)
    submitButton.click()
    await vi.waitFor(() => expect(wrapper.text()).toContain('请输入管理员姓名'))
    expect(wrapper.text()).toContain('请输入用户名')
    expect(wrapper.text()).toContain('请输入密码')
    expect(wrapper.text()).toContain('请选择角色')
    expect(registerAccount).not.toHaveBeenCalled()

    await fillRegistration(wrapper)
    await findButton(wrapper, '立即注册').trigger('click')
    await flushPromises()
    expect(registerAccount).not.toHaveBeenCalled()
    expect(router.currentRoute.value.path).toBe('/register')
  })

  it.each([
    ['超级管理员', 1],
    ['管理员', 2],
    ['普通用户', 3],
  ] as const)('选择%s后点击注册，只发送一次请求，角色值为数字%s', async (label, role) => {
    const { wrapper, router } = await openPage('/register')
    await fillRegistration(wrapper)
    await chooseRole(wrapper, label)
    await findButton(wrapper, '立即注册').trigger('click')
    await flushPromises()

    expect(registerAccount).toHaveBeenCalledTimes(1)
    expect(registerAccount).toHaveBeenCalledWith({
      name: '测试姓名',
      userName: 'test-account',
      passWord: 'test-password',
      role,
    })
    expect(router.currentRoute.value.path).toBe('/login')
    expect(router.currentRoute.value.query.userName).toBe('test-account')
    expect((wrapper.get('input[autocomplete="username"]').element as HTMLInputElement).value).toBe(
      'test-account',
    )
  })

  it('Enter产生的原生submit在同tick及请求期间重复触发时都只注册一次', async () => {
    let finishRegistration!: () => void
    vi.mocked(registerAccount).mockReturnValue(
      new Promise<void>((resolve) => {
        finishRegistration = resolve
      }),
    )
    const { wrapper, router } = await openPage('/register')
    await fillRegistration(wrapper)
    await chooseRole(wrapper, '管理员')

    // jsdom 不执行 Enter 的浏览器默认动作，直接派发其产生的 submit 事件。
    await Promise.all([
      wrapper.get('form').trigger('submit'),
      wrapper.get('form').trigger('submit'),
    ])
    await flushPromises()
    expect(registerAccount).toHaveBeenCalledTimes(1)
    expect(findButton(wrapper, '立即注册').attributes('disabled')).toBeDefined()
    await wrapper.get('form').trigger('submit')
    await flushPromises()
    expect(registerAccount).toHaveBeenCalledTimes(1)

    finishRegistration()
    await flushPromises()
    expect(router.currentRoute.value.path).toBe('/login')
  })

  it('重置清空输入、角色以及已有校验错误', async () => {
    const { wrapper } = await openPage('/register')
    await findButton(wrapper, '立即注册').trigger('click')
    await flushPromises()
    await fillRegistration(wrapper)
    await chooseRole(wrapper, '普通用户')
    await findButton(wrapper, '重置').trigger('click')
    await flushPromises()

    expect(
      wrapper.findAll('input').every((item) => (item.element as HTMLInputElement).value === ''),
    ).toBe(true)
    expect(wrapper.get('.el-select').text()).toContain('请选择')
    await vi.waitFor(() => expect(wrapper.find('.el-form-item__error').exists()).toBe(false))
    expect(registerAccount).not.toHaveBeenCalled()
  })
})

describe('登录表单交互', () => {
  it('同tick连续submit只登录一次，请求期间继续阻止重复提交', async () => {
    let finishLogin!: () => void
    vi.mocked(loginAccount).mockReturnValue(
      new Promise((resolve) => {
        finishLogin = () => resolve(loggedInUser)
      }),
    )
    const { wrapper, router } = await openPage('/login')
    await wrapper.get('input[autocomplete="username"]').setValue('test-account')
    await wrapper.get('input[autocomplete="current-password"]').setValue('test-password')
    await Promise.all([
      wrapper.get('form').trigger('submit'),
      wrapper.get('form').trigger('submit'),
    ])
    await flushPromises()
    expect(loginAccount).toHaveBeenCalledTimes(1)
    await wrapper.get('form').trigger('submit')
    await flushPromises()
    expect(loginAccount).toHaveBeenCalledTimes(1)
    finishLogin()
    await flushPromises()
    expect(router.currentRoute.value.path).toBe('/admin/roles')
  })

  it('校验空输入，重置清空已输入内容和错误提示', async () => {
    const { wrapper } = await openPage('/login')
    await wrapper.get('form').trigger('submit')
    await vi.waitFor(() => expect(wrapper.text()).toContain('请输入用户名'))
    expect(wrapper.text()).toContain('请输入密码')
    expect(loginAccount).not.toHaveBeenCalled()

    await wrapper.get('input[autocomplete="username"]').setValue('test-account')
    await wrapper.get('input[autocomplete="current-password"]').setValue('test-password')
    await findButton(wrapper, '重置').trigger('click')
    await flushPromises()
    expect(
      wrapper.findAll('input').every((item) => (item.element as HTMLInputElement).value === ''),
    ).toBe(true)
    await vi.waitFor(() => expect(wrapper.find('.el-form-item__error').exists()).toBe(false))
  })

  it('成功登录进入管理页，并在会话中保存返回的用户信息', async () => {
    const { wrapper, router } = await openPage('/login')
    await wrapper.get('input[autocomplete="username"]').setValue('  test-account  ')
    await wrapper.get('input[autocomplete="current-password"]').setValue('test-password')
    await findButton(wrapper, '本地登录').trigger('click')
    await flushPromises()

    expect(loginAccount).toHaveBeenCalledTimes(1)
    expect(loginAccount).toHaveBeenCalledWith({
      userName: 'test-account',
      passWord: 'test-password',
    })
    expect(router.currentRoute.value.path).toBe('/admin/roles')
    expect(wrapper.text()).toContain('角色列表测试页')
    expect(sessionStorage.getItem('hainan-admin-session')).toContain('test-token')
    expect(sessionStorage.getItem('hainan-admin-session')).not.toContain('test-password')
  })
})
