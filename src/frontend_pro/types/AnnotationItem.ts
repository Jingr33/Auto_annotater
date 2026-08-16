import type { ImagePredictionStatus } from "./ImagePredictionStatus";

export interface AnnotationItem {
  id: string;
  status: ImagePredictionStatus;
  created_at: string;
  updated_at: string;
}
