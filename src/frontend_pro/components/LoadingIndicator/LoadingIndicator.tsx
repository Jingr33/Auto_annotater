import { translations } from '../../translations/translations'

export interface LoadingIndicatorProps {
  message?: string
}

export const LoadingIndicator = ({ message = translations.loading.default }: LoadingIndicatorProps) => {
  return (
    <div className="loading-indicator">
      <p>{message}</p>
    </div>
  )
}
