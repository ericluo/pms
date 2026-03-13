import { ElMessage } from 'element-plus'

export class ApiError extends Error {
  constructor(
    public message: string,
    public status?: number,
    public code?: string
  ) {
    super(message)
    this.name = 'ApiError'
  }
}

/**
 * 处理 API 错误并显示用户友好的消息
 */
export function handleApiError(error: any, defaultMessage = '操作失败'): void {
  const message = error?.message || defaultMessage
  ElMessage.error(message)
  console.error('API Error:', error)
}

/**
 * 执行异步函数并统一处理错误
 */
export async function withErrorHandling<T>(
  fn: () => Promise<T>,
  defaultMessage = '操作失败'
): Promise<T> {
  try {
    return await fn()
  } catch (error: any) {
    handleApiError(error, defaultMessage)
    throw error
  }
}

/**
 * 验证表单数据并返回错误消息
 */
export function validateForm(
  validators: Array<{ condition: boolean; message: string }>
): string | null {
  for (const validator of validators) {
    if (validator.condition) {
      return validator.message
    }
  }
  return null
}
