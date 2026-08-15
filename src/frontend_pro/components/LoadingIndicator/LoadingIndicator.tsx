import { useTranslation } from 'react-i18next'

export interface LoadingIndicatorProps {
  message?: string
}

export const LoadingIndicator = ({ message }: LoadingIndicatorProps) => {
  const { t } = useTranslation()

  return (
    <div className="loading-indicator">
      <p>{message ?? t('loading.default')}</p>
    </div>
  )
}
