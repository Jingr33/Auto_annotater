import { Item, ItemListResponse, ImageUrlResponse, PipelineStatusResponse, ActionResult } from '../types/types'

const BASE_URL = '/api'

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const response = await fetch(`${BASE_URL}${path}`, {
    headers: { 'Content-Type': 'application/json' },
    ...options,
  })
  if (!response.ok) {
    throw new Error(`API error: ${response.status}`)
  }
  return response.json()
}

export const api = {
  getItems: () => request<ItemListResponse>('/items'),
  getItemImage: (itemId: string) => request<ImageUrlResponse>(`/items/${itemId}/image`),
  getPipelineStatus: () => request<PipelineStatusResponse>('/pipeline/status'),
  acceptItem: () => request<ActionResult>('/pipeline/accept', { method: 'POST' }),
  rejectItem: () => request<ActionResult>('/pipeline/reject', { method: 'POST' }),
  skipItem: () => request<ActionResult>('/pipeline/skip', { method: 'POST' }),
  goBack: () => request<ActionResult>('/pipeline/back', { method: 'POST' }),
}
