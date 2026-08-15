import { useTranslation } from 'react-i18next'
import { Box, Button, Paper, Stack } from '@mui/material'
import { usePipelineStatus } from '../../hooks/usePipelineStatus'
import { api } from '../../services/api'
import { LoadingIndicator } from '../LoadingIndicator/LoadingIndicator'
import { StatusBadge } from '../common/StatusBadge'

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

  const renderBadge = () => {
    if (status?.is_finished) {
      return <StatusBadge label={t('pipeline.finished')} tone="finished" />
    }

    if (status?.current_item_id) {
      return (
        <StatusBadge
          label={`${t('pipeline.currentPrefix')} ${status.current_item_id} (${status.total} ${t('pipeline.totalSuffix')})`}
          tone="active"
        />
      )
    }

    if (status?.is_waiting) {
      return <StatusBadge label={t('pipeline.waiting')} tone="waiting" />
    }

    return null
  }

  const canAct = Boolean(status?.current_item_id)

  return (
    <Paper variant="outlined">
      <Box sx={{ mb: 1.5 }}>{renderBadge()}</Box>

      <Stack direction="row" spacing={1}>
        <Button onClick={() => handleAction(api.goBack)} disabled={!canAct}>
          {t('pipeline.backButton')}
        </Button>

        <Button onClick={() => handleAction(api.skipItem)} disabled={!canAct}>
          {t('pipeline.skipButton')}
        </Button>

        <Button onClick={() => handleAction(api.rejectItem)} disabled={!canAct}>
          {t('pipeline.rejectButton')}
        </Button>

        <Button onClick={() => handleAction(api.acceptItem)} variant="contained" disabled={!canAct}>
          {t('pipeline.acceptButton')}
        </Button>
      </Stack>
    </Paper>
  )
}
