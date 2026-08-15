export interface PipelineStatusResponse {
  is_waiting: boolean
  is_finished: boolean
  total: number
  current_item_id: string | null
}
