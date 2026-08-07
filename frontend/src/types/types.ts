export type ImagePredictionStatus = 'pending' | 'accepted' | 'rejected'

export interface Item {
  id: string
  status: ImagePredictionStatus
  created_at: string
  updated_at: string
}

export interface ItemListResponse {
  items: Item[]
  total: number
}

export interface ImageUrlResponse {
  url: string
}

export interface PipelineStatusResponse {
  is_waiting: boolean
  is_finished: boolean
  total: number
  current_item_id: string | null
}

export interface ActionResult {
  success: boolean
}
