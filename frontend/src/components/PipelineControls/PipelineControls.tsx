import { usePipelineStatus } from '../../hooks/usePipelineStatus'
import { api } from '../../services/api'

export interface PipelineControlsProps {
  onRefresh: () => void
}

export const PipelineControls = ({ onRefresh }: PipelineControlsProps) => {
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
    return <div className="pipeline-controls">Loading pipeline status...</div>
  }

  return (
    <div className="pipeline-controls">
      <div className="status-info">
        {status?.is_finished ? (
          <span className="status-badge finished">Pipeline finished</span>
        ) : status?.current_item_id ? (
          <span className="status-badge active">
            Current: {status.current_item_id} ({status.total} total)
          </span>
        ) : status?.is_waiting ? (
          <span className="status-badge waiting">Waiting for items...</span>
        ) : null}
      </div>

      <div className="controls">
        <button
          onClick={() => handleAction(api.goBack)}
          disabled={!status?.current_item_id}
        >
          Back
        </button>
        <button
          onClick={() => handleAction(api.skipItem)}
          disabled={!status?.current_item_id}
        >
          Skip
        </button>
        <button
          onClick={() => handleAction(api.rejectItem)}
          disabled={!status?.current_item_id}
        >
          Reject
        </button>
        <button
          onClick={() => handleAction(api.acceptItem)}
          disabled={!status?.current_item_id}
        >
          Accept
        </button>
      </div>
    </div>
  )
}
