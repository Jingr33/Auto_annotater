import { Chip } from '@mui/material'

export type StatusTone = 'finished' | 'active' | 'waiting'

export interface StatusBadgeProps {
  label: string
  tone: StatusTone
}

const toneStyles: Record<StatusTone, { backgroundColor: string; color: string }> = {
  finished: { backgroundColor: '#d4edda', color: '#155724' },
  active: { backgroundColor: '#cce5ff', color: '#004085' },
  waiting: { backgroundColor: '#fff3cd', color: '#856404' },
}

export const StatusBadge = ({ label, tone }: StatusBadgeProps) => {
  return (
    <Chip
      label={label}
      size="small"
      sx={{
        backgroundColor: toneStyles[tone].backgroundColor,
        color: toneStyles[tone].color,
        fontWeight: 500,
      }}
    />
  )
}
