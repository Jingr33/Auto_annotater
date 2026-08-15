import { Stack, Typography } from '@mui/material'

export interface LicenseHeaderProps {
  title: string
  subtitle: string
}

export const LicenseHeader = ({ title, subtitle }: LicenseHeaderProps) => {
  return (
    <Stack spacing={2}>
      <Typography variant="h1">{title}</Typography>

      <Typography variant="body1" color="text.secondary">
        {subtitle}
      </Typography>
    </Stack>
  )
}
