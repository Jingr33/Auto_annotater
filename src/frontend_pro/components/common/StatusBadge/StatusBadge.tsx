import { Chip } from '@mui/material'

export type StatusTone = 'finished' | 'active' | 'waiting'

export interface StatusBadgeProps {
  label: string
  tone: StatusTone
}

const toneColor: Record<StatusTone, 'success' | 'info' | 'warning'> = {
  finished: 'success',
  active: 'info',
  waiting: 'warning',
}

export const StatusBadge = ({ label, tone }: StatusBadgeProps) => {
  return <Chip label={label} size="small" color={toneColor[tone]} />
}
