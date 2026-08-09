import { ImagePredictionStatus } from './ImagePredictionStatus'

export interface Item {
  id: string
  status: ImagePredictionStatus
  created_at: string
  updated_at: string
}
