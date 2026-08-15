import { Typography } from '@mui/material'

export interface LicenseHeaderProps {
  title: string
  subtitle: string
}

export const LicenseHeader = ({ title, subtitle }: LicenseHeaderProps) => {
  return (
    <>
      <Typography variant="h4" component="h1" sx={{ mb: 1 }}>
        {title}
      </Typography>
      <Typography variant="body1" color="text.secondary" sx={{ mb: 4 }}>
        {subtitle}
      </Typography>
    </>
  )
}
