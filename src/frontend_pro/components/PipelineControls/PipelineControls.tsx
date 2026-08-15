import { useTranslation } from 'react-i18next'
import { usePipelineStatus } from '../../hooks/usePipelineStatus'
import { api } from '../../services/api'
import { LoadingIndicator } from '../LoadingIndicator/LoadingIndicator'

export interface PipelineControlsProps {
  onRefresh: () => void
}

export const PipelineControls = ({ onRefresh }: PipelineControlsProps) => {
  const { t } = useTranslation()
  const { status, loading } = usePipelineStatus()

  const handleAction = async (action: () => Promise<unknown>) => {
    try {
      await action()
      onRefresh()
    } catch (err) {
      console.error('Action failed:', err)
    }
  }

  if (loading) {
    return <LoadingIndicator message={t('pipeline.loadingStatus')} />
  }

  return (
    <div className="pipeline-controls">
      <div className="status-info">
        {status?.is_finished ? (
          <span className="status-badge finished">{t('pipeline.finished')}</span>
        ) : status?.current_item_id ? (
          <span className="status-badge active">
            {t('pipeline.currentPrefix')} {status.current_item_id} ({status.total} {t('pipeline.totalSuffix')})
          </span>
        ) : status?.is_waiting ? (
          <span className="status-badge waiting">{t('pipeline.waiting')}</span>
        ) : null}
      </div>

      <div className="controls">
        <button
          onClick={() => handleAction(api.goBack)}
          disabled={!status?.current_item_id}
        >
          {t('pipeline.backButton')}
        </button>
        <button
          onClick={() => handleAction(api.skipItem)}
          disabled={!status?.current_item_id}
        >
          {t('pipeline.skipButton')}
        </button>
        <button
          onClick={() => handleAction(api.rejectItem)}
          disabled={!status?.current_item_id}
        >
          {t('pipeline.rejectButton')}
        </button>
        <button
          onClick={() => handleAction(api.acceptItem)}
          disabled={!status?.current_item_id}
        >
          {t('pipeline.acceptButton')}
        </button>
      </div>
    </div>
  )
}
